# Backend\servers\user\models\user.py

from beanie import Document, Field
from datetime import datetime

class User(Document):
    id: str
    name: str
    phone: str
    birth: datetime
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "users"
        indexes = [("id")]