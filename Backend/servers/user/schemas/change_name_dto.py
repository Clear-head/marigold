from pydantic import BaseModel
from starlette.responses import JSONResponse

class RequestChangeName(BaseModel):
    new_name: str

class ResponseChangeName(JSONResponse):
    status_code: int
    content: dict
