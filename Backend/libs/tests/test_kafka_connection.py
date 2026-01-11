"""
Kafka 연결 테스트 스크립트

로컬 환경에서 Docker Kafka와 연결을 테스트합니다.
"""

import asyncio
import os
from kafka.producer import KafkaProducer
from commons.logger import get_marigold_logger

logger = get_marigold_logger("kafka-connection-test")


async def test_kafka_connection():
    """Kafka 연결 및 메시지 전송 테스트"""

    # 현재 설정 확인
    from commons.settings import settings
    logger.info(f"현재 KAFKA_BOOTSTRAP_SERVERS: {settings.KAFKA_BOOTSTRAP_SERVERS}")

    # 로컬 테스트를 위한 환경변수 임시 설정
    original_kafka_url = os.getenv('KAFKA_BOOTSTRAP_SERVERS')

    # Docker 실행 시: kafka:9092 (내부 통신)
    # 로컬 실행 시: localhost:9092 (외부 접근)
    os.environ['KAFKA_BOOTSTRAP_SERVERS'] = 'localhost:9092'

    # settings 재로드
    from importlib import reload
    import commons.settings as settings_module
    reload(settings_module)
    from commons.settings import settings

    logger.info(f"변경된 KAFKA_BOOTSTRAP_SERVERS: {settings.KAFKA_BOOTSTRAP_SERVERS}")

    producer = KafkaProducer()

    try:
        logger.info("=== Kafka Producer 초기화 시작 ===")
        await producer.init_producer()
        logger.info("✅ Kafka Producer 초기화 성공!")

        # 테스트 메시지 전송
        logger.info("=== 테스트 메시지 전송 ===")
        message = {
            "event": "test_connection",
            "timestamp": "2024-01-12T00:00:00",
            "data": {"message": "Hello Kafka from local!"}
        }

        result = await producer.send_message(
            message=message,
            topic_name="test-connection-topic",
            key="test-key"
        )

        if result:
            logger.info("✅ 메시지 전송 성공!")
        else:
            logger.error("❌ 메시지 전송 실패")

        # 여러 메시지 전송 테스트
        logger.info("=== 10개 메시지 순차 전송 테스트 ===")
        success_count = 0
        for i in range(10):
            msg = {"id": i, "data": f"test_message_{i}"}
            if await producer.send_message(msg, "test-batch-topic", f"key-{i}"):
                success_count += 1

        logger.info(f"✅ {success_count}/10 메시지 전송 성공")

    except Exception as e:
        logger.error(f"❌ Kafka 연결 실패: {e}")
        logger.error(f"에러 타입: {type(e).__name__}")
        import traceback
        logger.error(f"상세 에러:\n{traceback.format_exc()}")

    finally:
        await producer.close()
        logger.info("Kafka Producer 종료")

        # 원래 환경변수 복원
        if original_kafka_url:
            os.environ['KAFKA_BOOTSTRAP_SERVERS'] = original_kafka_url


async def check_kafka_availability():
    """Kafka 서버 접근 가능 여부 확인"""
    import socket

    hosts = [
        ("localhost", 9092),
        ("127.0.0.1", 9092),
    ]

    logger.info("=== Kafka 서버 접근 가능 여부 확인 ===")

    for host, port in hosts:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()

            if result == 0:
                logger.info(f"✅ {host}:{port} 접근 가능")
            else:
                logger.warning(f"❌ {host}:{port} 접근 불가 (code: {result})")
        except Exception as e:
            logger.error(f"❌ {host}:{port} 확인 중 에러: {e}")


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("Kafka 연결 테스트")
    print("=" * 70 + "\n")
    print("⚠️  주의: Kafka 서버가 실행중이어야 합니다!")
    print("Docker: docker-compose up -d kafka")
    print("포트: localhost:9092")
    print("\n" + "=" * 70 + "\n")

    asyncio.run(check_kafka_availability())
    print("\n" + "=" * 70 + "\n")
    asyncio.run(test_kafka_connection())