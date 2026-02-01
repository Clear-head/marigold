from typing import List

from beanie import Document


class ChatRoom(Document):
    id: int
    members: List[str]

    class Settings:
        name = "chat_room"
        indexes = [("id", "members")]