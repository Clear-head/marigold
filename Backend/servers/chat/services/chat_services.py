from Backend.servers.chat.models.messages import BaseMessage
from Backend.servers.chat.repositories.message_repository import MessageRepository
from commons.logger import get_marigold_logger
from kafka.producer import kafka_producer
from kafka.topics import KafkaTopic


class ChatService:

    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.producer = kafka_producer
        self.message_repo = MessageRepository()
        self.topic = KafkaTopic.CHAT_MESSAGE

    async def send_message(self, room_id, message: BaseMessage):
        try:

            await self.message_repo.save_message(message)
            self.producer.publish_message(topic=self.topic, key=message.room_id, value=message)

        except Exception as e:
            self.logger.error(f"Failed to send message to room {room_id}: {e}")
            raise e

