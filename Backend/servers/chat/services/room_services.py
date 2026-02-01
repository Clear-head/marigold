from commons.logger import get_marigold_logger
from dto.chat_room_dto import InviteChatRoomDto
from kafka.producer import kafka_producer
from kafka.topics import KafkaTopic
from repositories.chat_room_repository import ChatRoomRepository


class RoomService:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.producer = kafka_producer
        self.repo = ChatRoomRepository()
        self.topic = KafkaTopic.CHAT_ROOM


    async def invite_user_to_rooms(self, request: InviteChatRoomDto):
        try:
            chat_room = await self.repo.get_rooms_by_user_id(request.sender_id)

            if len(chat_room) != 1:
                raise Exception
            chat_room = chat_room[0]
            chat_room.members.append(request.sender_id)
            await self.repo.update_room(room_id=chat_room.id, target_room=chat_room)
            await self.producer.publish_message(topic=self.topic, value=request.sender_id)
        except Exception as e:
            self.logger.error(f"Failed to invite user to room {request.room_id}: {e}")
            raise e

    async def create_chat_room(self):
        try:
            pass
        except Exception as e:
            self.logger.error(f"Failed to create chat room: {e}")
            raise e

    async def exit_chat_room(self):
        #   todo: 채팅방 인원 0 -> 삭제 로직 추가
        try:
            pass
        except Exception as e:
            self.logger.error(f"Failed to exit chat room: {e}")