from typing_extensions import override
from aiokafka import ConsumerRecord
from kafka.consumer import BaseKafkaConsumer
from kafka.events_schema import SignupRequest
from services.user_service import UserService


class AuthConsumer(BaseKafkaConsumer):
    def __init__(self, topic, consumer_group):
        super().__init__(topic=topic, consumer_group=consumer_group)
        self.service = UserService()


    @override
    async def handle_message(self, message: ConsumerRecord):
        try:
            if message.value.get('type') == "SIGNUP":
                dto = SignupRequest(**message.value)
                await self.service.signup(dto=dto)
        except Exception as e:
            raise e