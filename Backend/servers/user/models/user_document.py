# Backend\servers\user\models\user_document.py
# beanie

from datetime import datetime
from beanie import Document, Field

class User(Document):
    id: str
    name: str
    phone: str
    birth: datetime
    created_at: datetime = Field(default_factory=datetime.now)


    class Settings:
        name = "users"

