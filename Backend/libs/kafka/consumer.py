from abc import ABC, abstractmethod
from aiokafka import AIOKafkaConsumer
from aiokafka.errors import KafkaError

from commons.logger import get_marigold_logger
from commons.settings import settings

class BaseKafkaConsumer(ABC):
    def __init__(self, topic, consumer_group):
        self.topic = topic
        self.consumer_group = consumer_group
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS
        self.logger = get_marigold_logger(__name__)
        self._consumer = None
        self._running = True

    async def init_consumer(self):
        if self._consumer is None:
            self._consumer = AIOKafkaConsumer(
                self.topic,
                group_id=self.consumer_group,
                bootstrap_servers=self.bootstrap_servers,
            )
            await self._consumer.start()
            self.logger.info(f"Kafka Consumer started: {self.topic} in group {self.consumer_group}")

    @abstractmethod
    async def handle_message(self, msg):
        pass

    async def consume(self):
        await self.init_consumer()
        try:
            async for msg in self._consumer:
                if not self._running:
                    break
                try:
                    await self.handle_message(msg)
                except Exception as e:
                    self.logger.error(f"Error handling message: {e}")
        except KafkaError as ke:
            self.logger.error(f"Kafka error occurred: {ke}")
        finally:
            await self.close()

    async def stop(self):
        self._running = False

    async def close(self):
        if self._consumer:
            await self._consumer.stop() # close() 대신 stop() 사용 권장
            self.logger.info(f"Kafka Consumer closed: {self.topic}")