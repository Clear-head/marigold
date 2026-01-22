from datetime import datetime

from beanie import Document, PydanticObjectId


class BaseMessage(Document):
    id: str
    room_id: int = PydanticObjectId
    sender: str = PydanticObjectId
    content: str
    send_at: datetime

    class Settings:
        is_root = True
        name: str


class TextMessage(BaseMessage):
    class Settings:
        name = "text_messages"

class PhotoMessage(BaseMessage):
    meta: dict

    class Settings:
        name = "photo_messages"

class videoMessage(BaseMessage):
    meta: dict

    class Settings:
        name = "video_messages"