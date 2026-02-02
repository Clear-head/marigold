from datetime import datetime

from beanie import PydanticObjectId
from commons.logger import get_marigold_logger
from dto.chat_room_dto import InviteChatRoomDto, CreateChatRoomDto, ExiteChatRoomDto
from kafka.producer import kafka_producer
from kafka.topics import KafkaTopic

from models.chat_room import ChatRoom
from models.messages import TextMessage
from repositories.chat_room_repository import ChatRoomRepository
from services.chat_services import ChatService


class RoomService:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.producer = kafka_producer
        self.repo = ChatRoomRepository()
        self.topic = KafkaTopic.CHAT_ROOM
        self.chat = ChatService()


    async def invite_user_to_room(self, request: InviteChatRoomDto):
        try:
            chat_room = await self.repo.get_room_by_id(room_id=request.room_id)

            #   채팅방 못찾음
            if chat_room is None:
                raise Exception

            #   이미 있음
            #   todo: new error define
            if request.target_user_id in chat_room.members:
                raise Exception

            chat_room.members.append(request.target_user_id)

            await self.repo.update_room(room_id=chat_room.id, target_room=chat_room)

            msg = TextMessage(
                room_id=chat_room.id,
                sender_id="ADMIN",
                send_at=datetime.now(),
                content=f"{request.target_user_id}님이 입장하셨습니다."
            )

            await self.chat.send_message(str(chat_room.id), msg)


        except Exception as e:
            self.logger.error(f"Failed to invite user to room {request.room_id}: {e}")
            raise e

    async def create_chat_room(self, request: CreateChatRoomDto) -> str:
        try:
            new_room = ChatRoom(
                members=[request.creator_id]
            )
            created_room = await self.repo.create_room(new_room)
            return str(created_room.id)

        except Exception as e:
            self.logger.error(f"Failed to create chat room: {e}")
            raise e

    async def exit_chat_room(self, request: ExiteChatRoomDto):
        try:

            chat_room = await self.repo.get_room_by_id(room_id=request.room_id)

            if chat_room is None:
                raise Exception

            if request.exit_user_id not in chat_room.members:
                raise Exception

            chat_room.members.remove(request.exit_user_id)
            if not chat_room.members:
                await self.repo.remove_room(room_id=chat_room.id)
            else:
                await self.repo.update_room(room_id=chat_room.id, target_room=chat_room)

                msg = TextMessage(
                    room_id=chat_room.id,
                    sender_id="ADMIN",
                    send_at=datetime.now(),
                    content=f"{request.exit_user_id}님이 퇴장하셨습니다."
                )

                await self.chat.send_message(str(chat_room.id), message=msg)

        except Exception as e:
            self.logger.error(f"Failed to exit chat room: {e}")