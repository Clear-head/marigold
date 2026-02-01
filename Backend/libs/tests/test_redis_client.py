import asyncio
import os
from databases.redis_client import get_redis_client, close_redis_client
from commons.logger import get_marigold_logger

logger = get_marigold_logger("redis-test")


async def test_redis_connection():
    """Redis 연결 및 기본 동작 테스트"""

    # 로컬 테스트를 위한 환경변수 설정
    # Docker 실행 시: redis://redis:6379
    # 로컬 실행 시: redis://localhost:6379
    original_redis_url = os.getenv('REDIS_URL')

    # 로컬 테스트용 URL로 임시 변경
    os.environ['REDIS_URL'] = 'redis://:redispassword@localhost:6379'

    try:
        logger.info("=== Redis 연결 테스트 시작 ===")

        # 1. 연결 테스트
        logger.info("1. Redis 클라이언트 연결 중...")
        client = await get_redis_client()
        logger.info("✅ Redis 연결 성공!")

        # 2. PING 테스트
        logger.info("2. PING 테스트...")
        pong = await client.ping()
        logger.info(f"✅ PING 응답: {pong}")

        # 3. SET/GET 테스트
        logger.info("3. SET/GET 테스트...")
        await client.set('test_key', 'test_value', ex=10)
        value = await client.get('test_key')
        logger.info(f"✅ SET/GET 성공: {value}")

        # 4. 삭제 테스트
        logger.info("4. DELETE 테스트...")
        await client.delete('test_key')
        value = await client.get('test_key')
        logger.info(f"✅ DELETE 성공: {value is None}")

        # 5. 실시간 채팅용 기능 테스트
        logger.info("5. 실시간 채팅 기능 테스트...")

        # 5-1. List (메시지 큐)
        await client.rpush('chat:room:123', 'message1', 'message2')
        messages = await client.lrange('chat:room:123', 0, -1)
        logger.info(f"✅ 메시지 큐: {messages}")

        # 5-2. Hash (사용자 정보)
        await client.hset('user:1', mapping={
            'name': 'Alice',
            'status': 'online'
        })
        user_info = await client.hgetall('user:1')
        logger.info(f"✅ 사용자 정보: {user_info}")

        # 5-3. Sorted Set (읽지 않은 메시지)
        await client.zadd('unread:user:1', {'room:123': 5, 'room:456': 2})
        unread = await client.zrange('unread:user:1', 0, -1, withscores=True)
        logger.info(f"✅ 읽지 않은 메시지: {unread}")

        # 6. TTL 테스트
        logger.info("6. TTL (만료시간) 테스트...")
        await client.setex('temp_key', 5, 'temp_value')
        ttl = await client.ttl('temp_key')
        logger.info(f"✅ TTL: {ttl}초")

        # 정리
        await client.delete('chat:room:123', 'user:1', 'unread:user:1', 'temp_key')

        logger.info("=== ✅ 모든 테스트 통과! ===")

    except Exception as e:
        logger.error(f"❌ 테스트 실패: {e}")
        raise

    finally:
        # 연결 종료
        await close_redis_client()
        logger.info("Redis 연결 종료")

        # 원래 환경변수 복원
        if original_redis_url:
            os.environ['REDIS_URL'] = original_redis_url


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Redis 연결 테스트")
    print("="*60 + "\n")
    print("⚠️  주의: Redis 서버가 실행중이어야 합니다!")
    print("Docker: docker-compose up -d redis")
    print("또는")
    print("로컬: redis-server")
    print("\n" + "="*60 + "\n")

    asyncio.run(test_redis_connection())