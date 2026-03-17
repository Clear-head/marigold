from aiokafka import ConsumerRecord
from typing_extensions import override

from kafka.consumer import BaseKafkaConsumer
from kafka.events_schema import NotificationToOfflineUsers
from services.notice_service import NotificationService


class ChatConsumer(BaseKafkaConsumer):
    def __init__(self, topic: str, consumer_group: str):
        super().__init__(topic, consumer_group)
        self.service = NotificationService()


    @override
    async def handle_message(self, msg: ConsumerRecord) -> None:
        try:
            await self.service.send_notifications(
                NotificationToOfflineUsers(
                    **msg.value
                )
            )

        except Exception as e:
            self.logger.error(e)