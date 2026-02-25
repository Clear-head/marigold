from datetime import datetime

from beanie import PydanticObjectId
from pydantic import ValidationError

from commons.logger import get_marigold_logger
from dto.message_dto import MessageRequest, MessageTypeEnum
from models.messages import TextMessage, ImageMessage, VideoMessage
from services.chat_services import ChatService
from services.room_services import RoomService
from websocket.connection_manager import WSConnectionManager


class WebSocketHandler:
    """WebSocket 메시지 처리 핸들러"""

    def __init__(
        self,
        connection_manager: WSConnectionManager,
        chat_service: ChatService,
        room_service: RoomService
    ):
        self.logger = get_marigold_logger(__name__)
        self.connection_manager = connection_manager
        self.chat_service = chat_service
        self.room_service = room_service

    async def handle_message(self, user_id: str, data: dict) -> None:
        """
        메시지 타입별 라우팅

        Args:
            user_id: 발신자 ID (URL에서 추출)
            data: 클라이언트로부터 받은 메시지 데이터
        """
        # 메시지 타입 확인
        message_type = data.get("message_type") or data.get("type")

        try:
            # 메시지 처리 (text, image, video)
            if message_type in ["text", "image", "video"]:
                request = MessageRequest(**data)
                await self._handle_message(user_id, request)

            else:
                self.logger.warning(f"Unknown message type: {message_type} from user {user_id}")
                await self._send_error(user_id, f"Unknown message type: {message_type}")

        except ValidationError as e:
            self.logger.error(f"Validation error from user {user_id}: {e}")
            await self._send_error(user_id, f"Invalid message format: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error handling message from user {user_id}: {e}")
            await self._send_error(user_id, f"Internal error: {str(e)}")

    async def _handle_message(self, user_id: str, request: MessageRequest) -> None:
        """
        메시지 처리 (text/image/video)

        Args:
            user_id: 발신자 ID
            request: 메시지 요청 DTO
        """
        try:
            # room_id를 PydanticObjectId로 변환
            room_object_id = PydanticObjectId(request.room_id)

            # MessageRequest → Model 변환
            if request.message_type == MessageTypeEnum.TEXT:
                message = TextMessage(
                    room_id=room_object_id,
                    sender_id=user_id,
                    content=request.content,
                    send_at=datetime.now()
                )
            elif request.message_type == MessageTypeEnum.IMAGE:
                message = ImageMessage(
                    room_id=room_object_id,
                    sender_id=user_id,
                    media=request.media,
                    send_at=datetime.now()
                )
            elif request.message_type == MessageTypeEnum.VIDEO:
                message = VideoMessage(
                    room_id=room_object_id,
                    sender_id=user_id,
                    media=request.media,
                    send_at=datetime.now()
                )
            else:
                await self._send_error(user_id, f"Unsupported message type: {request.message_type}")
                return

            await self.chat_service.send_message(request.room_id, message)

            # DB에서 방 멤버 조회
            chat_room = await self.room_service.repo.get_room_by_id(room_id=request.room_id)
            if chat_room:
                # 실시간 브로드캐스트
                offline_users = await self.connection_manager.broadcast_to_users(
                    user_ids=chat_room.members,
                    message=message
                )

                #   오프라인 유저 알림
                await self.chat_service.send_message_to_offline(
                    user_id=offline_users,
                    room_id=request.room_id,
                    message=message
                )

            self.logger.info(f"Message sent: user={user_id}, room={request.room_id}, type={request.message_type}")

        except Exception as e:
            self.logger.error(f"Failed to handle message from user {user_id}: {e}")
            await self._send_error(user_id, "Failed to send message")
            raise

    async def _send_error(self, user_id: str, error_message: str) -> None:
        """
        사용자에게 에러 메시지 전송

        Args:
            user_id: 사용자 ID
            error_message: 에러 메시지
        """
        try:
            await self.connection_manager.send_personal_message(
                user_id=user_id,
                message={
                    "type": "error",
                    "message": error_message,
                    "timestamp": datetime.now().isoformat()
                }
            )
        except Exception as e:
            self.logger.error(f"Failed to send error message to user {user_id}: {e}")
