# Backend\servers\auth\services\login_service.py
# 로그인 서비스
from repositories.credential_repository import CredentialRepository
from commons.logger import get_marigold_logger
from exceptions.auth_exceptions import UserNotFoundException, InvalidPasswordException
from services.hasher import verify_password, hash_password

from exceptions.auth_exceptions import TokenExpiredException
from kafka.producer import KafkaProducer
from kafka.events_schema import SignupRequest as KafkaSR
from kafka.topics import USER_AUTH
from dto.dto import SignupRequest

from kafka.topics import KafkaTopic
from models import UserCredential

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
        raise e

async def signup(dto: SignupRequest):
    try:

        repo = CredentialRepository()
        credential = UserCredential(
            id=dto.user_id,
            password_hased=hash_password(dto.password),
        )

        repo.create_credential(credential)

        producer = KafkaProducer()
        kafka_signup = KafkaSR(
            user_id = dto.user_id,
            name = dto.name,
            phone = dto.phone,
            birth = dto.birth,
            created_at = dto.created_at,
        )
        await producer.publish_message(
            message=kafka_signup.model_dump(mode="json"),
            topics=KafkaTopic.USER_AUTH,
            key=dto.user_id,
        )

    except Exception as e:
        logger.error(e)
        raise e