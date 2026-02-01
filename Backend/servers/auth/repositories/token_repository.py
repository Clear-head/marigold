# Backend\servers\auth\repositories\token_repository.py
# beanie
# logger, client, document

from libs.commons.logger import get_marigold_logger
from typing import List
from libs.databases.redis_client import get_redis_client

class TokenRepository:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.client = get_redis_client()

    async def create_redis_item(self, key: str, value: str, **kwargs) -> bool:
        return await self.client.set(key, value, **kwargs)

    async def get_redis_item(self, key: str) -> str:
        return await self.client.get(key)
    
    async def delete_redis_item(self, key: str) -> bool:
        return await self.client.delete(key)
    
    async def update_redis_item(self, key: str, value: str, **kwargs) -> bool:
        return await self.client.set(key, value, **kwargs)


