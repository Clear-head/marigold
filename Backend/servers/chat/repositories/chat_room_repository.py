from typing import List, Optional
from beanie import PydanticObjectId
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

    async def get_rooms_by_user_id(self, user_id: PydanticObjectId) -> List[ChatRoom]:
        try:
            return await self.model.find(self.model.members == user_id).to_list()
        except Exception as e:
            self.logger.error(f"Failed to fetch rooms for user {user_id}: {e}")
            raise e

    async def remove_room(self, room_id: PydanticObjectId):
        try:
            room = await self.model.get(room_id)
            if room:
                await room.delete()
        except Exception as e:
            self.logger.error(f"Failed to remove room {room_id}: {e}")
            raise e

    async def add_member(self, room_id: PydanticObjectId, new_member: PydanticObjectId) -> Optional[ChatRoom]:
        try:
            room = await self.model.get(room_id)
            if room:
                await room.update({"$addToSet": {"members": new_member}})
                return room
            else:
                raise Exception(f"Room {room_id} not found")
        except Exception as e:
            self.logger.error(f"Failed to add member {new_member} to room {room_id}: {e}")
            raise e

    async def remove_member(self, room_id: PydanticObjectId, member_to_remove: PydanticObjectId) -> Optional[ChatRoom]:
        try:
            room = await self.model.get(room_id)
            if room:
                await room.update({"$pull": {"members": member_to_remove}})
                return room
            else:
                raise Exception(f"Failed to remove member {member_to_remove} from room {room_id}")
        except Exception as e:
            self.logger.error(f"Failed to remove member {member_to_remove} from room {room_id}: {e}")
            raise e