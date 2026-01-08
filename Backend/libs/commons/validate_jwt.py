import jwt

from Backend.libs.commons.logger import get_marigold_logger
from Backend.libs.databases.redis_client import get_redis_client
from Backend.libs.exceptions.auth_exceptions import (
    InvalidTokenException, NoActiveSessionException,
    RedisConnectionException, TokenExpiredException,
    TokenRevokedException, InvalidTokenTypeException
)
from settings import settings




class JWTValidator:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)

    async def _validate_jwt(self, token: str) -> dict:
        try:
            # JWT 디코딩 및 기본 검증
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
                issuer=settings.JWT_ISSUER
            )

            # 2단계 검증: Redis 세션 확인
            if check_session:
                user_id = payload.get("userId")
                if not user_id:
                    raise InvalidTokenException("Missing userId in token")

                try:
                    redis = await get_redis_client()
                    # 해당 유저가 활성 세션을 가지고 있는지 확인
                    session_count = await redis.zcard(f"user_tokens:{user_id}")

                    if session_count == 0:
                        raise NoActiveSessionException()

                except NoActiveSessionException:
                    raise
                except Exception as e:
                    self.logger.error(f"Redis error during session check: {e}")
                    raise RedisConnectionException(str(e))

            return payload

        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()

        except jwt.InvalidTokenError as e:
            raise InvalidTokenException(f"Invalid token: {str(e)}")

        except (InvalidTokenException, TokenExpiredException, NoActiveSessionException) as e:
            raise e

        except Exception as e:
            self.logger.error(f"Unexpected error during token verification: {e}")
            raise InvalidTokenException(f"Token verification failed: {str(e)}")

    async def verify_jwt_http(self, authorization: str) -> dict:
        """
        HTTP Authorization 헤더를 파싱하고 토큰을 검증

        Args:
            authorization: "Bearer {token}" 형식의 Authorization 헤더

        Returns:
            토큰 페이로드

        Raises:
            InvalidTokenException: Bearer 형식 오류 또는 검증 실패
        """
        if not authorization or not authorization.startswith("Bearer "):
            raise InvalidTokenException("Invalid authorization header format")

        token = authorization.replace("Bearer ", "").strip()

        return await self._validate_jwt(token)

    async def verify_jwt_websocket(self, websocket) -> dict:
        """
        WebSocket 연결에서 토큰을 추출, 검증

        Args:
            websocket: FastAPI WebSocket 객체

        Returns:
            토큰 페이로드

        Raises:
            InvalidTokenException: 토큰 없음 또는 검증 실패

        Note:
            실패 시 자동으로 WebSocket 연결을 종료합니다 (code: 4401)
        """
        token = websocket.query_params.get("token")

        if not token:
            await websocket.close(code=4401, reason="Token missing")
            raise InvalidTokenException("Token missing in query parameters")

        try:
            payload = await self._validate_jwt(token, check_session=False)
            return payload

        except Exception as e:
            self.logger.error(f"WebSocket error during token verification: {e}")
            await websocket.close(code=4401, reason=str(e))
            raise e