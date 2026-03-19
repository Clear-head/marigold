from firebase_admin import messaging
from firebase_admin.messaging import Message, Notification, MulticastMessage

from kafka.events_schema import NotificationToOfflineUsers
from repositories.fcm_repository import FCMRepository


class NotificationService:

    def __init__(self):
        self.repository = FCMRepository()

    async def send_notifications(self, request: NotificationToOfflineUsers):
        try:

            user_tokens = await self.repository.get_tokens_by_user_ids(request.user_ids)

            await messaging.send_each_for_multicast_async(
                MulticastMessage(
                    notification=Notification(
                        title=request.sender_id,
                        body=request.message_preview
                    ),
                    tokens=user_tokens
                )
            )

        except Exception as e:
            raise e

    async def delete_token(self, user_id: str):
        try:
            await self.repository.delete_tokens_by_user_id(user_id)
        except Exception as e:
            raise e

    async def upsert_token(self, user_id: str, device_id: str, fcm_token: str, platform: str):
        try:
            await self.repository.upsert_token(user_id, device_id, fcm_token, platform)
        except Exception as e:
            raise e

    async def delete_token_by_device(self, user_id: str, device_id: str):
        try:
            await self.repository.delete_token_by_device(user_id, device_id)
        except Exception as e:
            raise e