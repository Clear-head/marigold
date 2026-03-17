from pydantic import BaseModel
from datetime import datetime

class RequestChangeBirth(BaseModel):
    birth: datetime

class ResponseChangeBirth(BaseModel):
    status_code: int
    content: dict

