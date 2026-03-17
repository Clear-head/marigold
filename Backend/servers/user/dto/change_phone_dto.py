from pydantic import BaseModel

class RequestChangePhone(BaseModel):
    new_phone: str

class ResponseChangePhone(BaseModel):
    status_code: int
    content: dict

