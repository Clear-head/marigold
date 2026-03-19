from enum import Enum
from typing import Literal

from pydantic import BaseModel


class SearchType(str, Enum):
    Phone = "Phone"
    Name = "Name"
    ID = "ID"

class RequestUserInfoDTO(BaseModel):
    search_type: Literal["Phone", "Name", "ID"]
    target_user_info: str

class ResponseUserInfoDTO(BaseModel):
    target_user_id: str
    name: str
    phone: str
    birth: str