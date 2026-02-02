from typing import List, Optional

from beanie import Document, PydanticObjectId


class ChatRoom(Document):
    id: Optional[PydanticObjectId] = None
    members: List[str]

    class Settings:
        name = "chat_room"
        indexes = [("members",)]