import json
from aiokafka import AIOKafkaProducer
from commons.logger import get_marigold_logger
from commons.settings import settings


class KafkaProducer:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self._client = None

    async def init_producer(self):
        try:
            self._client = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                acks='all',
                # compression_type='lz4',
                max_batch_size=16384,
                linger_ms=10,
            )
            await self._client.start()
            self.logger.info("Kafka producer initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize Kafka producer: {e}")
            self._client = None
            raise e

    async def send_message(self, message: dict, topic_name: str, key: str):
        try:

            await self._client.send_and_wait(topic=topic_name, value=message, key=key)
            return True

        except Exception as e:
            self.logger.error(f"kafka error : {e}")
            return False

    async def close(self):
        if self._client is not None:
            try:
                await self._client.stop()
                self.logger.info("Kafka producer closed successfully")
            except Exception as e:
                self.logger.error(f"Error closing Kafka producer: {e}")
            finally:
                self._client = None
        else:
            self.logger.warning("Kafka producer not initialized")

kafka_producer = KafkaProducer()