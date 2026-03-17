# Backend\servers\auth\services\hasher.py
# password 해시 서비스
# bcrypt

from commons.logger import get_marigold_logger
from bcrypt import hashpw, gensalt, checkpw
from exceptions.auth_exceptions import InvalidPasswordException

logger = get_marigold_logger(__name__)

async def hash_password(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

async def verify_password(input_password: str, hashed_password: str) -> bool:
    return checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))    
