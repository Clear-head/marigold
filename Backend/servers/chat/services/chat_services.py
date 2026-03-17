from datetime import datetime

from commons.logger import get_marigold_logger

from chat_exceptions.message_exceptions import MessageSendFailedException
from kafka.events_schema import NotificationToOfflineUsers
from kafka.producer import kafka_producer
from kafka.topics import KafkaTopic
from models.messages import BaseMessage, TextMessage, ImageMessage, VideoMessage
from repositories.message_repository import MessageRepository


class ChatService:

    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.producer = kafka_producer
        self.message_repo = MessageRepository()
        self.topic = KafkaTopic.CHAT_MESSAGE

    async def send_message(self, room_id: str, message: BaseMessage):
        try:
            # 전송 시간 설정
            if message.send_at is None:
                message.send_at = datetime.now()

            # DB에 메시지 저장
            saved_message = await self.message_repo.save_message(message)

            # Kafka로 메시지 발행
            message_dict = saved_message.model_dump(mode='json')
            publish_success = await self.producer.publish_message(
                topic=self.topic,
                key=room_id,
                message=message_dict
            )

            if not publish_success:
                self.logger.warning(f"Failed to publish message to Kafka for room {room_id}")

            return saved_message

        except Exception as e:
            self.logger.error(f"Failed to send message to room {room_id}: {e}")
            raise MessageSendFailedException(reason=str(e))

    async def send_message_to_offline(self, user_id: list[str], message: BaseMessage, room_id: str):
        try:
            if isinstance(message, TextMessage):
                msg_type, msg_preview = "text", message.content
            elif isinstance(message, ImageMessage):
                msg_type, msg_preview = "image", "[이미지]"
            else:
                msg_type, msg_preview = "video", "[동영상]"

            event = NotificationToOfflineUsers(
                user_ids=user_id,
                room_id=room_id,
                sender_id=message.sender_id,
                message_type=msg_type,
                message_preview=msg_preview,
                sent_at=message.send_at,
            )

            #   notification 으로 발행
            publish_success = await self.producer.publish_message(
                topic=KafkaTopic.NOTIFICATION_PUSH,
                key=room_id,
                message=event.model_dump(mode='json'),
            )

            if not publish_success:
                self.logger.warning(f"Failed to publish message to Kafka for room {room_id}")

        except Exception as e:
            self.logger.error(f"Failed to send message to room {room_id}: {e}")

    async def get_messages(self, room_id: str, last_msg_id: str = None, limit: int = 20):
        try:
            return await self.message_repo.get_messages_by_room_id(room_id, last_msg_id, limit)

        except Exception as e:
            self.logger.error(f"Failed to get messages from room {room_id}: {e}")
            raise e

