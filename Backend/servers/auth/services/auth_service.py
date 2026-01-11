# Backend\servers\auth\services\auth_service.py
# 인증 서비스

from libs.commons.logger import get_marigold_logger
from repositories.token_repository import TokenRepository
from libs.commons.validate_jwt import JWTValidator
from libs.commons.settings import settings
from datetime import datetime, timedelta
import jwt
from libs.exceptions.auth_exceptions import TokenExpiredException

class IssueJWTService:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.token_repository = TokenRepository()
        self.validator = JWTValidator()

    async def _create_access_token(self, user_id: str) -> str:
        now = datetime.now()
        exp = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        payload = {
            "userId": user_id,
            "exp": int(exp.timestamp()),
            "iat": int(now.timestamp()),
            "iss": settings.JWT_ISSUER,
            "type": "access"
        }

        access_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return access_token

    async def _create_refresh_token(self, user_id: str) -> str:
        now = datetime.now()
        exp = now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

        payload = {
            "userId": user_id,
            "exp": int(exp.timestamp()),
            "iat": int(now.timestamp()),
            "iss": settings.JWT_ISSUER,
            "type": "refresh"
        }

        refresh_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return refresh_token

    async def refresh_token(self, user_id: str, refresh_token: str) -> str:
        try:
            if not await self.validator.verify_jwt_http(refresh_token):
                raise TokenExpiredException("Refresh token expired")

            
            access_token = await self._create_access_token(user_id)
            refresh_token = await self._create_refresh_token(user_id)
            
            await self.token_repository.update_redis_item(f"refresh_token:{refresh_token}", user_id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }

        except TokenExpiredException:
            self.logger.error(f"Refresh token expired")
            raise TokenExpiredException("Refresh token expired")

        except Exception as e:
            self.logger.error(f"Unexpected error during refresh token: {e}")
            raise e(f"Refresh token verification failed: {str(e)}")
        
        
        

