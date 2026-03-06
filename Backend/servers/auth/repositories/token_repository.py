# Backend\servers\auth\repositories\token_repository.py
# beanie
# logger, client, document

from commons.logger import get_marigold_logger
from typing import List
from databases.redis_client import get_redis_client

class TokenRepository:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)

    async def create_redis_item(self, key: str, value: str, **kwargs) -> bool:
        client = await get_redis_client()
        return await client.set(key, value, **kwargs)

    async def get_redis_item(self, key: str) -> str:
        client = await get_redis_client()
        return await client.get(key)

    async def delete_redis_item(self, key: str) -> bool:
        client = await get_redis_client()
        return await client.delete(key)

    async def update_redis_item(self, key: str, value: str, **kwargs) -> bool:
        client = await get_redis_client()
        return await client.set(key, value, **kwargs)


