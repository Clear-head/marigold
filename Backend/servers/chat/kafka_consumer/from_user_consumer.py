from aiokafka import ConsumerRecord
from kafka.consumer import BaseKafkaConsumer
from typing_extensions import override

from services.room_services import RoomService


class UserConsumer(BaseKafkaConsumer):
    def __init__(self, topic, consumer_group):
        super().__init__(topic, consumer_group)
        self.room_service = RoomService()

    @override
    async def handle_message(self, msg: ConsumerRecord):
        try:
            if msg.value.get('type') == "DELETE_USER":
                await self.room_service.exit_all_chat_room(user_id=msg.value.get("user_id"))
        except Exception as e:
            raise e
