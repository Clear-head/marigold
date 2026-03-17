from pydantic import BaseModel

class RequestChangeName(BaseModel):
    new_name: str

class ResponseChangeName(BaseModel):
    status_code: int
    content: dict
