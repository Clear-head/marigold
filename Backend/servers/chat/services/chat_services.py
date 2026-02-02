from datetime import datetime

from models.messages import BaseMessage
from repositories.message_repository import MessageRepository
from commons.logger import get_marigold_logger
from kafka.producer import kafka_producer
from kafka.topics import KafkaTopic


class ChatService:

    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.producer = kafka_producer
        self.message_repo = MessageRepository()
        self.topic = KafkaTopic.CHAT_MESSAGE

    async def send_message(self, room_id: str, message: BaseMessage):
        try:

            if message.send_at is None:
                message.send_at = datetime.now()

            await self.message_repo.save_message(message)

            message_dict = message.model_dump(mode='json')

            await self.producer.publish_message(topic=self.topic, key=room_id, message=message_dict)

        except Exception as e:
            self.logger.error(f"Failed to send message to room {room_id}: {e}")
            raise e

