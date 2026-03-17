from asyncio import gather
from datetime import datetime

from commons.logger import get_marigold_logger
from kafka.producer import kafka_producer
from kafka.topics import KafkaTopic

from dto.chat_room_dto import InviteChatRoomDto, CreateChatRoomDto, ExitChatRoomDto, ResponseGetChatRoomDto
from chat_exceptions.room_exceptions import (
    RoomNotFoundException,
    UserAlreadyInRoomException,
    UserNotInRoomException
)
from models.chat_room import ChatRoom
from models.messages import TextMessage
from repositories.chat_room_repository import ChatRoomRepository
from repositories.message_repository import MessageRepository
from services.chat_services import ChatService


class RoomService:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.producer = kafka_producer
        self.repo = ChatRoomRepository()
        self.chat_repo = MessageRepository()
        self.topic = KafkaTopic.CHAT_ROOM
        self.chat_service = ChatService()


    async def get_rooms(self, user_id: str) -> ResponseGetChatRoomDto:
        """사용자가 속한 채팅방 목록 조회"""
        try:
            chat_rooms = await self.repo.get_rooms_by_user_id(user_id)
            return ResponseGetChatRoomDto(rooms=chat_rooms)

        except Exception as e:
            self.logger.error(f"Failed to get rooms for user {user_id}: {e}")
            raise


    async def invite_user_to_room(self, request: InviteChatRoomDto):
        """채팅방에 사용자 초대"""
        try:
            chat_room = await self.repo.get_room_by_id(room_id=request.room_id)

            # 채팅방을 찾을 수 없음
            if chat_room is None:
                raise RoomNotFoundException(room_id=request.room_id)

            # 이미 채팅방에 있음
            if request.target_user_id in chat_room.members:
                raise UserAlreadyInRoomException(
                    room_id=request.room_id,
                    user_id=request.target_user_id
                )

            # 멤버 추가
            chat_room.members.append(request.target_user_id)
            await self.repo.update_room(room_id=str(chat_room.id), target_room=chat_room)

            # 입장 메시지 전송
            msg = TextMessage(
                room_id=chat_room.id,
                sender_id="ADMIN",
                send_at=datetime.now(),
                content=f"{request.target_user_id}님이 입장하셨습니다."
            )
            await self.chat_service.send_message(str(chat_room.id), msg)

        except (RoomNotFoundException, UserAlreadyInRoomException) as e:
            raise e
        except Exception as e:
            self.logger.error(f"Failed to invite user to room {request.room_id}: {e}")
            raise e

    async def create_chat_room(self, request: CreateChatRoomDto) -> str:
        """새로운 채팅방 생성"""
        try:
            new_room = ChatRoom(members=request.members)
            created_room = await self.repo.create_room(new_room)
            return str(created_room.id)

        except Exception as e:
            self.logger.error(f"Failed to create chat room: {e}")
            raise

    async def exit_chat_room(self, request: ExitChatRoomDto):
        """채팅방 나가기"""
        try:
            chat_room = await self.repo.get_room_by_id(room_id=request.room_id)

            # 채팅방을 찾을 수 없음
            if chat_room is None:
                raise RoomNotFoundException(room_id=request.room_id)

            # 채팅방에 없는 사용자
            if request.exit_user_id not in chat_room.members:
                raise UserNotInRoomException(
                    room_id=request.room_id,
                    user_id=request.exit_user_id
                )

            # 멤버 제거
            chat_room.members.remove(request.exit_user_id)

            # 멤버가 없으면 채팅방 삭제, 있으면 업데이트
            if not chat_room.members:
                await gather(
                    self.chat_repo.delete_all_messages_in_room(room_id=str(chat_room.id)),
                    self.repo.remove_room(room_id=str(chat_room.id))
                )
            else:
                await self.repo.update_room(room_id=str(chat_room.id), target_room=chat_room)

        except (RoomNotFoundException, UserNotInRoomException) as e:
            raise e

        except Exception as e:
            self.logger.error(f"Failed to exit chat room: {e}")
            raise e

    async def exit_all_chat_room(self, user_id: str):
        """유저 탈퇴 시 전부 삭제"""
        try:
            exit_dtos = [
                ExitChatRoomDto(
                    exit_user_id=user_id,
                    room_id=str(i.id)
                )
                for i in await self.repo.get_rooms_by_user_id(user_id)
            ]
            await gather(
                *[self.exit_chat_room(dto) for dto in exit_dtos]
            )

        except (RoomNotFoundException, UserNotInRoomException) as e:
            raise e
