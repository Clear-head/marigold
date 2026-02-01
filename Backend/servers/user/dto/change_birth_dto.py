from pydantic import BaseModel
from starlette.responses import JSONResponse
from datetime import datetime

class RequestChangeBirth(BaseModel):
    birth: datetime

class ResponseChangeBirth(JSONResponse):
    status_code: int
    content: dict

