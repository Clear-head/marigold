from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class MessageTypeEnum(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"


class MediaMeta(BaseModel):
    file_url: str
    file_name: str
    file_size: int  # bytes
    mime_type: str
    width: int | None = None
    height: int | None = None
    thumbnail_url: str | None = None
    duration: float | None = None  # VIDEO 전용


class MessageDTO(BaseModel):
    message_type: MessageTypeEnum
    room_id: str
    sender_id: str
    send_at: datetime
    content: str | None = None      # TEXT 전용
    media: MediaMeta | None = None  # IMAGE, VIDEO 전용
