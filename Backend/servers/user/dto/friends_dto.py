from pydantic import BaseModel


class FriendDto(BaseModel):
    target_user_id: str