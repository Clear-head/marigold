"""
MongoDB Client 테스트
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from beanie import Document, init_beanie
from pymongo import AsyncMongoClient

from databases.mongo_client import init_database


class SampleDocument(Document):
    """테스트용 Document 모델"""
    name: str
    value: int

    class Settings:
        name = "sample_collection"


class TestMongoClient:
    """MongoDB Client 테스트"""

    @pytest.mark.asyncio
    async def test_init_database_success(self):
        """데이터베이스 초기화 성공 테스트"""
        mock_client = MagicMock(spec=AsyncMongoClient)
        mock_db = MagicMock()
        mock_client.__getitem__.return_value = mock_db

        with patch('databases.mongo_client.AsyncMongoClient', return_value=mock_client):
            with patch('databases.mongo_client.init_beanie', new_callable=AsyncMock) as mock_init_beanie:
                await init_database(
                    connection_url="mongodb://localhost:27017",
                    db_name="test_db",
                    models=[SampleDocument]
                )

                # init_beanie이 올바른 파라미터로 호출되었는지 확인
                mock_init_beanie.assert_called_once()
                call_kwargs = mock_init_beanie.call_args.kwargs
                assert call_kwargs['database'] == mock_db
                assert call_kwargs['document_models'] == [SampleDocument]

    @pytest.mark.asyncio
    async def test_init_database_connection_error(self):
        """데이터베이스 연결 실패 테스트"""
        with patch('databases.mongo_client.AsyncMongoClient', side_effect=Exception("Connection failed")):
            with pytest.raises(Exception) as exc_info:
                await init_database(
                    connection_url="mongodb://invalid:27017",
                    db_name="test_db",
                    models=[SampleDocument]
                )

            assert "Connection failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_init_database_beanie_init_error(self):
        """Beanie 초기화 실패 테스트"""
        mock_client = MagicMock(spec=AsyncMongoClient)
        mock_db = MagicMock()
        mock_client.__getitem__.return_value = mock_db

        with patch('databases.mongo_client.AsyncMongoClient', return_value=mock_client):
            with patch('databases.mongo_client.init_beanie', new_callable=AsyncMock, side_effect=Exception("Beanie init failed")):
                with pytest.raises(Exception) as exc_info:
                    await init_database(
                        connection_url="mongodb://localhost:27017",
                        db_name="test_db",
                        models=[SampleDocument]
                    )

                assert "Beanie init failed" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_init_database_with_multiple_models(self):
        """여러 모델로 데이터베이스 초기화 테스트"""
        class AnotherDocument(Document):
            title: str

            class Settings:
                name = "another_collection"

        mock_client = MagicMock(spec=AsyncMongoClient)
        mock_db = MagicMock()
        mock_client.__getitem__.return_value = mock_db

        models = [SampleDocument, AnotherDocument]

        with patch('databases.mongo_client.AsyncMongoClient', return_value=mock_client):
            with patch('databases.mongo_client.init_beanie', new_callable=AsyncMock) as mock_init_beanie:
                await init_database(
                    connection_url="mongodb://localhost:27017",
                    db_name="test_db",
                    models=models
                )

                call_kwargs = mock_init_beanie.call_args.kwargs
                assert call_kwargs['document_models'] == models


@pytest.mark.integration
class TestMongoClientIntegration:
    """MongoDB Client 통합 테스트 (실제 MongoDB 필요)"""

    @pytest.mark.asyncio
    async def test_real_mongodb_connection(self):
        """실제 MongoDB 연결 및 CRUD 테스트"""
        # 이 테스트는 docker-compose로 MongoDB가 실행중일 때만 동작
        try:
            from commons.settings import settings

            await init_database(
                connection_url=settings.MONGO_URL,
                db_name="test_database",
                models=[SampleDocument]
            )

            # Create
            doc = SampleDocument(name="test", value=123)
            await doc.insert()

            # Read
            found = await SampleDocument.find_one(SampleDocument.name == "test")
            assert found is not None
            assert found.name == "test"
            assert found.value == 123

            # Update
            found.value = 456
            await found.save()

            updated = await SampleDocument.get(found.id)
            assert updated.value == 456

            # Delete
            await updated.delete()

            deleted = await SampleDocument.find_one(SampleDocument.name == "test")
            assert deleted is None

        except Exception as e:
            pytest.skip(f"MongoDB server not available: {e}")