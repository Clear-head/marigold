"""
pytest 공통 설정 및 fixture
"""

import pytest
import asyncio
import os
import sys
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch


# 테스트 환경 설정
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """테스트 환경 초기화"""
    # 로그 디렉토리를 현재 디렉토리로 변경
    test_log_dir = Path(__file__).parent / "test_logs"
    test_log_dir.mkdir(exist_ok=True)

    # 환경변수 설정 (로거가 사용)
    os.environ["LOG_DIR"] = str(test_log_dir)

    # Kafka 로컬 테스트를 위한 환경변수 설정
    # Docker 내부: kafka:9092
    # 로컬 테스트: localhost:9092
    if "KAFKA_BOOTSTRAP_SERVERS" not in os.environ:
        os.environ["KAFKA_BOOTSTRAP_SERVERS"] = "localhost:9092"

    yield

    # 테스트 후 정리 (선택사항)
    # import shutil
    # shutil.rmtree(test_log_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    세션 스코프의 이벤트 루프 생성
    비동기 테스트에서 공유 사용
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_settings():
    """테스트용 설정 모킹"""
    settings = MagicMock()
    settings.REDIS_URL = "redis://:test_password@localhost:6379/0"
    settings.MONGO_URL = "mongodb://test_user:test_pass@localhost:27017"
    settings.MONGO_DB_NAME = "test_database"
    settings.KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

    return settings


@pytest.fixture(autouse=True)
def reset_singletons():
    """
    각 테스트 실행 전 싱글톤 인스턴스 초기화
    """
    # Redis 클라이언트 초기화
    try:
        import databases.redis_client as redis_client
        redis_client._redis_client = None
    except ImportError:
        pass

    # Kafka Producer 초기화
    try:
        import kafka.producer as kafka_prod
        kafka_prod.kafka_producer._client = None
    except ImportError:
        pass

    yield

    # 테스트 후 정리
    try:
        import databases.redis_client as redis_client
        redis_client._redis_client = None
    except ImportError:
        pass

    try:
        import kafka.producer as kafka_prod
        kafka_prod.kafka_producer._client = None
    except ImportError:
        pass


@pytest.fixture
def mock_logger():
    """로거 Mock - 파일 시스템 에러 방지"""
    with patch('commons.logger.get_marigold_logger') as mock:
        mock_logger_instance = MagicMock()
        mock.return_value = mock_logger_instance
        yield mock_logger_instance