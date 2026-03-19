from beanie import Document


class Friendship(Document):
    user_id: str
    friends: list[str] = []
    ban: list[str] = []

    class Settings:
        name = "friendship"
        indexes = [("user_id",)]