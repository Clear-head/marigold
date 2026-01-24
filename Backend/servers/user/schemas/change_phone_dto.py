from pydantic import BaseModel
from starlette.responses import JSONResponse

class RequestChangePhone(BaseModel):
    new_phone: str
    password: str

class ResponseChangePhone(JSONResponse):
    status_code: int
    content: dict

