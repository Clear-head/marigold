from typing import List

from beanie import Document, PydanticObjectId


class ChatRoom(Document):
    id: PydanticObjectId
    members: List[str]

    class Settings:
        name = "chat_room"
        indexes = [("members",)]