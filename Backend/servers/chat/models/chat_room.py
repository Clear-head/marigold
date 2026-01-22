from typing import List

from beanie import Document, PydanticObjectId


class ChatRoom(Document):
    id: str
    members: List[PydanticObjectId]

    class Settings:
        name = "chat_room"
        indexes = [("id", "members")]