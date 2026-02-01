# Backend\servers\auth\services\login_service.py
# 로그인 서비스

from repositories.credential_repository import CredentialRepository
from libs.commons.logger import get_marigold_logger
from libs.exceptions.auth_exceptions import UserNotFoundException, InvalidPasswordException
from services.hasher import verify_password

logger = get_marigold_logger(__name__)

# 우선 리턴은 bool값으로 받지만 추후 수정 가능
# TODO: 파일명 auth_service.py 변경 및 클래스화, 비밀번호 변경 로직 추가가
async def login(user_id: str, password: str) -> bool:
    try:
        credential_repository = CredentialRepository()
        user_credential = await credential_repository.get_credential_by_id(user_id)

        if not user_credential:
            raise UserNotFoundException("User not found")
        if not await verify_password(password, user_credential.password_hased):
            raise InvalidPasswordException("Invalid password")
        return True

    except UserNotFoundException:
        logger.error(f"User not found")
        raise UserNotFoundException("User not found")
        
    except InvalidPasswordException:
        logger.error(f"Invalid password")
        raise InvalidPasswordException("Invalid password")

    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        raise e(f"Login failed: {str(e)}")

    