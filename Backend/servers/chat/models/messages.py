from datetime import datetime

from beanie import Document
from pydantic import BaseModel


class MediaMeta(BaseModel):
    """Embedded document for media metadata"""
    file_url: str
    file_name: str
    file_size: int  # bytes
    mime_type: str
    width: int | None = None
    height: int | None = None
    thumbnail_url: str | None = None
    duration: float | None = None  # VIDEO 전용


class BaseMessage(Document):
    room_id: int
    sender_id: str
    send_at: datetime

    class Settings:
        is_root = True


class TextMessage(BaseMessage):
    content: str

    class Settings:
        name = "text_messages"


class ImageMessage(BaseMessage):
    media: MediaMeta

    class Settings:
        name = "image_messages"


class VideoMessage(BaseMessage):
    media: MediaMeta

    class Settings:
        name = "video_messages"