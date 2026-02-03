from typing import List

from beanie import PydanticObjectId
from models.messages import BaseMessage
from commons.logger import get_marigold_logger


class MessageRepository:
    def __init__(self):
        self.model = BaseMessage
        self.logger = get_marigold_logger(__name__)

    async def save_message(self, message: BaseMessage) -> BaseMessage:
        """메시지 저장"""
        try:
            return await message.insert()
        except Exception as e:
            self.logger.error(f"Failed to insert message: {e}", exc_info=True)
            raise

    async def get_messages_by_room_id(self, room_id: str, last_message_id: str = None, limit: int = 20) -> List[BaseMessage]:
        """채팅방의 메시지 목록 조회 (페이지네이션 지원)"""
        try:
            room_oid = PydanticObjectId(room_id)

            # last_message_id가 있으면 해당 메시지 이전의 메시지들을 가져옴 (페이지네이션)
            if last_message_id:
                last_msg_oid = PydanticObjectId(last_message_id)
                return await self.model.find(
                    self.model.room_id == room_oid,
                    self.model.id < last_msg_oid
                ).sort("-send_at").limit(limit).to_list()
            else:
                # 최신 메시지부터 limit 개수만큼 가져옴
                return await self.model.find(
                    self.model.room_id == room_oid
                ).sort("-send_at").limit(limit).to_list()

        except Exception as e:
            self.logger.error(f"Failed to read messages for room {room_id}: {e}", exc_info=True)
            raise

    async def update_message(self, message: BaseMessage):
        """메시지 업데이트"""
        try:
            return await message.save()
        except Exception as e:
            self.logger.error(f"Failed to update message {message.id}: {e}", exc_info=True)
            raise

    async def delete_one_message(self, message: BaseMessage):
        """메시지 삭제"""
        try:
            return await message.delete()
        except Exception as e:
            self.logger.error(f"Failed to delete message {message.id}: {e}", exc_info=True)
            raise

    async def delete_all_messages_in_room(self, room_id: str):
        """채팅방의 모든 메시지 삭제"""
        try:
            oid = PydanticObjectId(room_id)
            await self.model.find(self.model.room_id == oid).delete()
        except Exception as e:
            self.logger.error(f"Failed to delete all messages in room {room_id}: {e}", exc_info=True)
            raise