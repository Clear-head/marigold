# Backend\servers\auth\dto\dto.py
from datetime import datetime

from pydantic import BaseModel

class LoginRequest(BaseModel):
    user_id: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class SignupRequest(BaseModel):
    user_id: str
    password: str
    name: str
    phone: str
    birth: datetime
    created_at: datetime