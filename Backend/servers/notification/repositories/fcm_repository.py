from datetime import datetime, UTC
from typing import Literal

from beanie.operators import In

from commons.logger import get_marigold_logger
from models.firebase_token import FCM

logger = get_marigold_logger(__name__)


class FCMRepository:
    async def upsert_token(self, user_id: str, device_id: str, fcm_token: str, platform: Literal["android", "ios"]) -> FCM:
        try:
            existing = await FCM.find_one(
                FCM.user_id == user_id,
                FCM.device_id == device_id,
            )
            if existing:
                await existing.set({
                    FCM.fcm_token: fcm_token,
                    FCM.platform: platform,
                    FCM.updated_at: datetime.now(UTC),
                })
                return existing
            return await FCM(
                user_id=user_id,
                device_id=device_id,
                fcm_token=fcm_token,
                platform=platform,
                updated_at=datetime.now(UTC),
            ).insert()
        except Exception as e:
            logger.error(f"Failed to upsert FCM token for user {user_id}: {e}", exc_info=True)
            raise

    async def get_tokens_by_user_ids(self, user_ids: list[str]) -> list[str]:
        try:
            docs = await FCM.find(In(FCM.user_id, user_ids)).to_list()
            return [doc.fcm_token for doc in docs]
        except Exception as e:
            logger.error(f"Failed to fetch FCM tokens for users {user_ids}: {e}", exc_info=True)
            raise

    async def delete_tokens_by_user_id(self, user_id: str) -> None:
        try:
            await FCM.find(FCM.user_id == user_id).delete()
        except Exception as e:
            logger.error(f"Failed to delete FCM tokens for user {user_id}: {e}", exc_info=True)
            raise

    async def delete_token_by_device(self, user_id: str, device_id: str) -> None:
        try:
            await FCM.find(FCM.user_id == user_id, FCM.device_id == device_id).delete()
        except Exception as e:
            logger.error(f"Failed to delete FCM token for user {user_id}, device {device_id}: {e}", exc_info=True)
            raise