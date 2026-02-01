from pydantic import BaseModel


class InviteChatRoomDto(BaseModel):
    room_id: int
    target_user_id: str
    sender_id: str


class ExiteChatRoomDto(BaseModel):
    room_id: int
    exit_user_id: str


class CreateChatRoomDto(BaseModel):
    room_id: int
    creator_id: str