# Backend/servers/user/services/user_service.py

from repositories.user_repository import UserRepository
from libs.commons.logger import get_marigold_logger

from dto.change_name_dto import RequestChangeName, ResponseChangeName
from dto.change_phone_dto import RequestChangePhone, ResponseChangePhone
from dto.change_birth_dto import RequestChangeBirth, ResponseChangeBirth

class UserService:
    # TODO 
    # 1. 이름 변경
    # 2. 전화번호 변경
    # 3. 생일 변경
    
    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.repo = UserRepository()
    
    async def change_name(self, name_info: RequestChangeName, user_id: str):
        """
            User 이름 변경 로직
        """
        target_user = await self.repo.get_user_by_id(user_id)
        target_user.name = name_info.new_name
        await self.repo.update_user(user_id, target_user)
        return ResponseChangeName(
            status_code = 200,
            content = {
                'msg': f'Changed name to {target_user.name}'
                }
        )

    async def change_phone(self, phone_info: RequestChangePhone, user_id: str):
        """
            User 전화번호 변경 로직
        """
        target_user = await self.repo.get_user_by_id(user_id)
        target_user.phone = phone_info.new_phone
        await self.repo.update_user(user_id, target_user)
        return ResponseChangePhone(
            status_code = 200,
            content = {
                'msg' : f'Changed phone-number to {target_user.phone}'
            }
        )

    async def change_birth(self, birth_info: RequestChangeBirth, user_id: str):
        """
            User 생일 변경 로직
        """
        target_user = await self.repo.get_user_by_id(user_id)
        target_user.birth = birth_info.new_birth
        await self.repo.update_user(user_id, target_user)
        return ResponseChangeBirth(
            status_code = 200,
            content = {
                'msg' : f'Changed birth to {target_user.birth}'
            }
        )
        