from typing import List

from Backend.servers.chat.models.chat_room import ChatRoom
from commons.logger import get_marigold_logger


class ChatRoomRepository:
    def __init__(self):
        self.model = ChatRoom
        self.logger = get_marigold_logger(__name__)

    async def create_room(self, new_room: ChatRoom) -> ChatRoom:
        try:
            return await new_room.insert()
        except Exception as e:
            self.logger.error(f"Room creation failed: {e}")
            raise e

    async def get_rooms_by_user_id(self, user_id: str) -> List[ChatRoom]:
        try:
            return await self.model.find(self.model.members == user_id).to_list()
        except Exception as e:
            self.logger.error(f"Failed to fetch rooms for user {user_id}: {e}")
            raise e

    async def remove_room(self, room_id: int):
        try:
            room = await self.model.get(room_id)
            if room:
                await room.delete()
        except Exception as e:
            self.logger.error(f"Failed to remove room {room_id}: {e}")
            raise e

    async def update_room(self, room_id: int, target_room: ChatRoom):
        try:
            await self.model.update_one(self.model.room_id == room_id, target_room)
        except Exception as e:
            self.logger.error(f"Failed to update room {room_id}: {e}")
            raise e