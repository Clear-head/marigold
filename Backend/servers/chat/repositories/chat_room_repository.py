from typing import List

from beanie import PydanticObjectId
from models.chat_room import ChatRoom
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

    async def get_room_by_id(self, room_id: str) -> ChatRoom | None:
        try:
            oid = PydanticObjectId(room_id)
            return await self.model.get(oid)
        except Exception as e:
            self.logger.error(f"Failed to fetch room {room_id}: {e}")
            raise e

    async def remove_room(self, room_id: str):
        try:
            oid = PydanticObjectId(room_id)
            room = await self.model.get(oid)
            if room:
                await room.delete()
        except Exception as e:
            self.logger.error(f"Failed to remove room {room_id}: {e}")
            raise e

    async def update_room(self, room_id: str, target_room: ChatRoom):
        try:
            await target_room.save()
        except Exception as e:
            self.logger.error(f"Failed to update room {room_id}: {e}")
            raise e