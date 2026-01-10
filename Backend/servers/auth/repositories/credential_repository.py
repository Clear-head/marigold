# Backend\servers\auth\repositories\credential_repository.py
# beanie
# logger, client, document

from libs.commons.logger import get_marigold_logger
from models.credential import UserCredential
from libs.databases.mongo_client import get_mongo_client
from typing import List

class CredentialRepository:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.client = get_mongo_client()
        self.document = UserCredential

    async def create_credential(self, credential: UserCredential) -> UserCredential:
        return await self.document.insert_one(credential)
    
    async def update_credential(self, credential_id: str, credential: UserCredential) -> UserCredential:
        return await self.document.update_one(self.document.id == credential_id, credential)
    
    async def delete_credential(self, credential_id: str) -> UserCredential:
        return await self.document.delete_one(self.document.id == credential_id)
    
    async def get_all_credentials(self) -> List[UserCredential]:
        return await self.document.find_all().to_list()
    
    async def get_credential_by_name(self, name: str) -> UserCredential:
        return await self.document.find_one(self.document.name == name)
    
    async def get_credential_by_id(self, id: str) -> UserCredential:
        return await self.document.find_one(self.document.id == id)
