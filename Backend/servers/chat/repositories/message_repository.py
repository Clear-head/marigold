from typing import List

from Backend.servers.chat.models.messages import BaseMessage
from commons.logger import get_marigold_logger


class MessageRepository:
    def __init__(self):
        self.model = BaseMessage
        self.logger = get_marigold_logger(__name__)

    async def save_message(self, message: BaseMessage) -> BaseMessage:
        try:
            return await message.insert()
        except Exception as e:
            self.logger.error(f"Failed to insert message: {e}")
            raise e

    async def get_messages_by_room_id(self, room_id: int, limit: int = 50) -> List[BaseMessage]:
        try:
            return await self.model.find(
                self.model.room_id == room_id
            ).sort("-send_at").limit(limit).to_list()
        except Exception as e:
            self.logger.error(f"Failed to read messages for room {room_id}: {e}")
            raise e

    async def update_message(self, message: BaseMessage):
        try:
            return await message.save()
        except Exception as e:
            self.logger.error(f"Failed to update message {message.id}: {e}")
            raise e

    async def delete_one_message(self, message: BaseMessage):
        try:
            return await message.delete()
        except Exception as e:
            self.logger.error(f"Failed to delete message {message.id}: {e}")
            raise e

    async def delete_all_messages_in_room(self, room_id: int):
        try:
            await self.model.find(self.model.room_id == room_id).delete()
        except Exception as e:
            self.logger.error(f"Failed to delete all messages in room {room_id}: {e}")
            raise e