"""
Redis Client Manager

전역 Redis 연결을 관리합니다.
Connection Pool을 사용하여 효율적인 연결 관리를 제공합니다.
"""

from redis.asyncio import Redis, RedisError
from commons.settings import settings
from commons.logger import get_marigold_logger

logger = get_marigold_logger("redis-client")

_redis_client: Redis = None


async def get_redis_client() -> Redis:
    global _redis_client

    if _redis_client is None:
        try:
            _redis_client = await Redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,  # 자동으로 bytes -> str 변환
                max_connections=10,      # Connection Pool 크기
                socket_connect_timeout=5,
                socket_keepalive=True
            )

            # 연결 테스트
            await _redis_client.ping()
            logger.info("Redis connection established successfully")

        except RedisError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            _redis_client = None
            raise e
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise e.with_traceback(e.__traceback__)

    return _redis_client


# async def close_redis_client():
#     global _redis_client
#
#     if _redis_client:
#         try:
#             await _redis_client.aclose()  # close() → aclose()
#             logger.info("Redis connection closed")
#         except Exception as e:
#             logger.error(f"Error closing Redis connection: {e}")
#         finally:
#             _redis_client = None