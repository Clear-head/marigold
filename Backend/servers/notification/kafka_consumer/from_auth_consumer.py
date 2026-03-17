from typing_extensions import override

from aiokafka import ConsumerRecord

from kafka.consumer import BaseKafkaConsumer
from services.notice_service import NotificationService


class UserConsumer(BaseKafkaConsumer):
    def __init__(self, topic, consumer_group):
        super().__init__(topic, consumer_group)
        self.service = NotificationService()


    @override
    async def handle_message(self, msg: ConsumerRecord):
        try:
            if msg.value.get("type") == "DELETE_USER":
                await self.service.delete_token(user_id=msg.value.get("user_id"))
            else:
                await self.service.upsert_token(**msg.value)

        except Exception as e:
            self.logger.error(e)