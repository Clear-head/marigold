from typing import List

from pydantic import BaseModel

from models.chat_room import ChatRoom


class InviteChatRoomDto(BaseModel):
    room_id: str
    target_user_id: str
    sender_id: str


class ExiteChatRoomDto(BaseModel):
    room_id: str
    exit_user_id: str


class CreateChatRoomDto(BaseModel):
    members: List[str]  #   user id


class ResponseGetChatRoomDto(BaseModel):
    rooms: List[ChatRoom]