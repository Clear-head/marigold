from datetime import datetime
from typing import Optional, Literal

from beanie import Document, PydanticObjectId


class FCM(Document):
    id: Optional[PydanticObjectId] = None
    user_id: str
    device_id: str
    fcm_token: str
    platform: Literal["android", "ios"]
    updated_at: datetime

    class Settings:
        name = "device_token"
        indexes = [
            ("user_id",),
            ("user_id", "device_id"),
        ]