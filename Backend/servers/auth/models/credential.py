# Backend\servers\auth\models\credential.py
# 로그인 로그아웃 보안 관리

from datetime import datetime
from beanie import Document, Field

class UserCredential(Document):
    id: str
    password_hased: str
    name: str

    class Settings:
        name = "user_credentials"

