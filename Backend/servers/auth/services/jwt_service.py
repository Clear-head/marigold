from datetime import datetime, timedelta
from typing import Tuple
from uuid import uuid4

import jwt

from commons.logger import get_marigold_logger
from commons.settings import settings
from commons.validate_jwt import JWTValidator
from databases.redis_client import get_redis_client
from exceptions.auth_exceptions import TokenRevokedException, InvalidTokenException, InvalidTokenTypeException, \
    RedisConnectionException

logger = get_marigold_logger(__name__)
validator = JWTValidator()


async def create_tokens(user_id: str) -> Tuple[str, str]:
    """
    Access Token과 Refresh Token을 생성합니다.

    Args:
        user_id: 사용자 ID

    Returns:
        (access_token, refresh_token) 튜플

    Example:
        access, refresh = await create_tokens("user_123")
    """
    access_token = await create_access_token(user_id)
    refresh_token = await create_refresh_token(user_id)

    logger.info(f"Tokens created for user: {user_id}")
    return access_token, refresh_token


async def create_access_token(user_id: str) -> str:
    """
    Access Token을 생성합니다 (Stateless, JTI 없음).

    Args:
        user_id: 사용자 ID

    Returns:
        JWT Access Token
    """
    now = datetime.now()
    exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "userId": user_id,
        "exp": int(exp.timestamp()),
        "iat": int(now.timestamp()),
        "iss": settings.JWT_ISSUER,
        "type": "access"
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


async def create_refresh_token(user_id: str) -> str:
    """
    Refresh Token을 생성합니다 (JTI 포함).

    Args:
        user_id: 사용자 ID

    Returns:
        JWT Refresh Token
    """
    now = datetime.now()
    exp = now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    jti = str(uuid4())

    payload = {
        "userId": user_id,
        "jti": jti,
        "exp": int(exp.timestamp()),
        "iat": int(now.timestamp()),
        "iss": settings.JWT_ISSUER,
        "type": "refresh"
    }

    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    # Redis에 저장 및 기기 제한 적용
    await store_refresh_token(jti, user_id)
    await enforce_device_limit(user_id, jti)

    return token

async def store_refresh_token(jti: str, user_id: str) -> None:
    """
    Refresh Token을 Redis에 저장합니다.

    Args:
        jti: JWT ID
        user_id: 사용자 ID

    Raises:
        RedisConnectionException: Redis 연결 실패
    """
    try:
        redis = await get_redis_client()

        # refresh_token:{jti} → user_id (TTL: REFRESH_TOKEN_EXPIRE_MINUTES)
        ttl = settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
        await redis.setex(
            f"refresh_token:{jti}",
            ttl,
            user_id
        )

        logger.debug(f"Stored refresh token: {jti} for user: {user_id}")

    except Exception as e:
        logger.error(f"Failed to store refresh token: {e}")
        raise RedisConnectionException(str(e))


async def revoke_refresh_token(jti: str) -> None:
    """
    특정 Refresh Token을 무효화합니다 (로그아웃).

    Args:
        jti: JWT ID

    Raises:
        RedisConnectionException: Redis 연결 실패
    """
    try:
        redis = await get_redis_client()

        # user_id 가져오기
        user_id = await redis.get(f"refresh_token:{jti}")

        if user_id:
            # refresh_token 삭제
            await redis.delete(f"refresh_token:{jti}")

            # user_tokens에서 제거
            await redis.zrem(f"user_tokens:{user_id}", jti)

            logger.info(f"Revoked refresh token: {jti} for user: {user_id}")
        else:
            logger.warning(f"Attempted to revoke non-existent token: {jti}")

    except Exception as e:
        logger.error(f"Failed to revoke refresh token: {e}")
        raise RedisConnectionException(str(e))


async def revoke_all_user_tokens(user_id: str) -> None:
    """
    사용자의 모든 Refresh Token을 무효화합니다 (전체 로그아웃).

    Args:
        user_id: 사용자 ID

    Raises:
        RedisConnectionException: Redis 연결 실패
    """
    try:
        redis = await get_redis_client()

        # 모든 JTI 가져오기
        jtis = await redis.zrange(f"user_tokens:{user_id}", 0, -1)

        if jtis:
            # 각 refresh_token 삭제
            for jti in jtis:
                await redis.delete(f"refresh_token:{jti}")

            # user_tokens 삭제
            await redis.delete(f"user_tokens:{user_id}")

            logger.info(f"Revoked all tokens ({len(jtis)}) for user: {user_id}")
        else:
            logger.warning(f"No tokens found for user: {user_id}")

    except Exception as e:
        logger.error(f"Failed to revoke all user tokens: {e}")
        raise RedisConnectionException(str(e))


async def enforce_device_limit(user_id: str, new_jti: str) -> None:
    """
    3개 기기 제한을 적용합니다.

    최대 기기 수를 초과하면 가장 오래된 토큰을 자동으로 제거합니다.

    Args:
        user_id: 사용자 ID
        new_jti: 새로 발급된 JWT ID

    Raises:
        RedisConnectionException: Redis 연결 실패
    """
    try:
        redis = await get_redis_client()

        # Sorted Set에 추가 (score: 현재 타임스탬프)
        await redis.zadd(
            f"user_tokens:{user_id}",
            {new_jti: datetime.now().strftime("%Y%m%d%H%M%S")},
        )

        # 현재 기기 수 확인
        count = await redis.zcard(f"user_tokens:{user_id}")

        # 최대 개수 초과 시 가장 오래된 것 제거
        if count > settings.MAX_DEVICES_PER_USER:
            # 가장 오래된 JTI 가져오기
            oldest_jtis = await redis.zrange(f"user_tokens:{user_id}", 0, 0)

            if oldest_jtis:
                oldest_jti = oldest_jtis[0]

                # refresh_token 삭제
                await redis.delete(f"refresh_token:{oldest_jti}")

                # user_tokens에서 제거
                await redis.zrem(f"user_tokens:{user_id}", oldest_jti)

                logger.info(f"Removed oldest token due to device limit: {oldest_jti}")

    except Exception as e:
        logger.error(f"Failed to enforce device limit: {e}")
        raise RedisConnectionException(str(e))


# ==================== 토큰 갱신 ====================

async def refresh_access_token(refresh_token: str) -> str:
    """
    Refresh Token으로 새로운 Access Token을 발급합니다.

    Args:
        refresh_token: Refresh Token

    Returns:
        새로운 Access Token

    Raises:
        InvalidTokenException: 토큰 검증 실패
        InvalidTokenTypeException: Refresh Token이 아님
        TokenRevokedException: 로그아웃된 토큰
    """
    # Refresh Token 검증
    payload = await validator._validate_jwt(refresh_token)

    # type 확인
    if payload.get("type") != "refresh":
        raise InvalidTokenTypeException(expected="refresh", received=payload.get("type"))

    # JTI 확인
    jti = payload.get("jti")
    if not jti:
        raise InvalidTokenException("Missing jti in refresh token")

    # Redis에서 존재 여부 확인 (로그아웃 확인)
    try:
        redis = await get_redis_client()
        user_id = await redis.get(f"refresh_token:{jti}")

        if not user_id:
            raise TokenRevokedException("Refresh token has been revoked")

        # 새로운 Access Token 생성
        new_access_token = await create_access_token(user_id)

        logger.info(f"Refreshed access token for user: {user_id}")
        return new_access_token

    except TokenRevokedException:
        raise
    except Exception as e:
        logger.error(f"Failed to refresh access token: {e}")
        raise RedisConnectionException(str(e))