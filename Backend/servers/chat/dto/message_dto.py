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


# WebSocket 클라이언트 요청용 DTO
class MessageRequest(BaseModel):
    """
    WebSocket으로 받는 메시지 요청 (클라이언트 → 서버)

    sender_id와 send_at은 서버에서 자동 생성되므로 포함하지 않음
    """
    message_type: MessageTypeEnum
    room_id: str
    content: str | None = None      # TEXT 전용
    media: MediaMeta | None = None  # IMAGE, VIDEO 전용


# 서버 응답 및 DB 저장용 DTO
class MessageDTO(BaseModel):
    message_type: MessageTypeEnum
    room_id: str  # MongoDB ObjectId as string
    sender_id: str
    send_at: datetime
    content: str | None = None      # TEXT 전용
    media: MediaMeta | None = None  # IMAGE, VIDEO 전용
