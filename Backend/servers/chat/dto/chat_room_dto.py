from pydantic import BaseModel


class InviteChatRoomDto(BaseModel):
    room_id: str
    target_user_id: str
    sender_id: str


class ExiteChatRoomDto(BaseModel):
    room_id: str
    exit_user_id: str


class CreateChatRoomDto(BaseModel):
    creator_id: str