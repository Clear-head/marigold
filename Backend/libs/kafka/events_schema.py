from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class NotificationToOfflineUsers(BaseModel):
    """
    오프라인 유저 알림
    chat -> notification
    topic: NOTIFICATION_PUSH
    """
    user_ids: list[str]
    room_id: str
    sender_id: str
    message_type: str       # text, image, video
    message_preview: str    # 알림에 표시할 미리보기 텍스트
    sent_at: datetime


class SignupRequest(BaseModel):
    """
    회원가입
    auth -> user
    topic: USER_AUTH
    """
    type: Literal["SIGNUP"] = "SIGNUP"
    user_id: str
    name: str
    phone: str
    birth: str
    created_at: datetime


class WithdrawRequest(BaseModel):
    """
    회원 탈퇴
    auth -> user, room & chat
    topic: USER_PROFILE
    """
    type: Literal["DELETE_USER"] = "DELETE_USER"
    user_id: str
    withdrawn_at: datetime


class AIRequest(BaseModel):
    """
    ai 서비스 이용
    chat -> ai
    topic: AI_REQUEST
    """
    pass

class CalendarNotification(BaseModel):
    """
    캘린더 일정 알림
    calendar -> notification
    topic: CALENDAR_EVENT
    """
    pass