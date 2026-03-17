# Backend\servers\user\models\user.py

from beanie import Document
from datetime import datetime

class User(Document):
    id: str
    name: str
    phone: str
    birth: datetime
    created_at: datetime = datetime.now()

    class Settings:
        name = "users"
        indexes = [("id")]