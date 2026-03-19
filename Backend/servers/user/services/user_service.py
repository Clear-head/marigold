# Backend/servers/user/services/user_service.py
import asyncio

from repositories.user_repository import UserRepository
from repositories.friends_repository import FriendsRepository
from commons.logger import get_marigold_logger
from kafka.events_schema import SignupRequest

from dto.change_name_dto import RequestChangeName, ResponseChangeName
from dto.change_phone_dto import RequestChangePhone, ResponseChangePhone
from dto.change_birth_dto import RequestChangeBirth, ResponseChangeBirth
from models.user import User
from models.friendship import Friendship
from dto.read_user_dto import SearchType, ResponseUserInfoDTO, RequestUserInfoDTO


class UserService:
    # TODO 
    # 1. 이름 변경
    # 2. 전화번호 변경
    # 3. 생일 변경
    
    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.repo = UserRepository()
        self.friend_repo = FriendsRepository()

    async def get_user_info(self, request: RequestUserInfoDTO) -> list[ResponseUserInfoDTO]:
        search_map = {
            SearchType.Phone: self.repo.get_user_by_phone,
            SearchType.ID: self.repo.get_user_by_id,
            SearchType.Name: self.repo.get_user_by_name,
        }

        search_func = search_map.get(request.search_type)

        user = await search_func(request.target_user_info)

        if request.search_type != SearchType.Name:
            return [
                ResponseUserInfoDTO(
                    target_user_id=str(user.id),
                    name=user.name,
                    phone=user.phone,
                    birth=user.birth
                )
            ]
        else:
            return [
                ResponseUserInfoDTO(
                    target_user_id=str(u.id),
                    name=u.name,
                    phone=u.phone,
                    birth=u.birth
                ) for u in user
            ]
    
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

    async def signup(self, dto: SignupRequest):
        try:
            new_user = User(
                id = dto.user_id,
                name = dto.name,
                phone = dto.phone,
                birth = dto.birth,
                created_at = dto.created_at,
            )

            new_friendship = Friendship(
                user_id = dto.user_id,
                friends = [],
                ban = []
            )

            await asyncio.gather(
                self.repo.create_user(new_user),
                self.friend_repo.create_friends(new_friendship),
            )

        except Exception as e:
            self.logger.error(e)
            raise e