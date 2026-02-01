from redis.asyncio import Redis, RedisError
from commons.settings import settings
from commons.logger import get_marigold_logger

logger = get_marigold_logger(__name__)

_redis_client: Redis = None


async def get_redis_client() -> Redis:
    """
        Redis: 전역 Redis 클라이언트 인스턴스
    """
    global _redis_client

    if _redis_client is None:
        try:
            _redis_client = Redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,  # bytes -> str 자동 변환
                max_connections=10,  # 실시간 채팅: 높은 동시성 처리
                socket_connect_timeout=5,  # 5초 연결 타임아웃
                socket_keepalive=True,  # TCP keep-alive 활성화
                health_check_interval=30,  # 30초마다 연결 상태 확인
                retry_on_timeout=True,  # 타임아웃 시 자동 재시도
            )

            # 연결 테스트 (비동기)
            await _redis_client.ping()
            logger.info("Redis connection established successfully")

        except RedisError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            _redis_client = None
            raise e
        except Exception as e:
            logger.error(f"Unexpected error connecting to Redis: {e}")
            _redis_client = None
            raise e

    return _redis_client


async def close_redis_client():
    """
    Redis 연결 종료 (graceful shutdown)
    """
    global _redis_client

    if _redis_client:
        try:
            await _redis_client.aclose()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")
        finally:
            _redis_client = None