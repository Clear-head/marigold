from datetime import datetime, timedelta

from pydantic import BaseModel, field_validator

"""

    Chat Service

"""
class SendTextMessage(BaseModel):
    """단순 텍스트 채팅"""
    room_id: int
    sender_id: str
    content: str
    send_at: str = datetime.now()
    type: str = "text"


class RequestCreateChatRoom(BaseModel):
    creator_id: str


class InvitedRoom(BaseModel):
    creator_id: str
    room_id: int
    invited_user_id: str
    invited_at: datetime



"""

    User Service

"""
class Register(BaseModel):
    id: str
    password: str
    name: str
    phone: str
    created_at: datetime = datetime.now()
    birth: datetime

    @field_validator("created_at")
    def validate_created_at(cls, value):
        if value < (datetime.now() - timedelta(minutes=15)):
            raise Exception("time error")
        return value


class Login(BaseModel):
    id: str
    password: str


"""

    Notification Service

"""
class UserStatus(BaseModel):
    user_id: str
    is_active: bool