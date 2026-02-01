# Backend\servers\user\repositories\user_repository.py
# beanie
# logger, client, document

from libs.commons.logger import get_marigold_logger
from models.user_document import User
from libs.databases.mongo_client import get_mongo_client
from typing import List

class UserRepository:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.client = get_mongo_client()
        self.document = User

    async def create_user(self, user:User) -> User:
        return await self.document.create(user)
    
    async def update_user(self, user_id:str, user:User) -> User:
        return await self.document.update_one(self.document.id == user_id, user)

    async def delete_user(self, user_id:str) -> User:
        return await self.document.delete_one(self.document.id == user_id)

    async def get_user_by_name(self, user_name: str) -> List[User]:
        return await self.document.find_all(self.document.name == user_name).to_list()
    
    async def get_user_by_id(self, user_id: str) -> User:
        return await self.document.find_one(self.document.id == user_id)