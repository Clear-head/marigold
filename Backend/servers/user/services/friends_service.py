from asyncio import gather, Semaphore
from fastapi import HTTPException


from dto.friends_dto import FriendDto
from commons.logger import get_marigold_logger
from repositories.friends_repository import FriendsRepository
from repositories.user_repository import UserRepository
from models.user import User


logger = get_marigold_logger(__name__)
repo = FriendsRepository()
user_repo = UserRepository()

async def get_friends(user_id: str) -> list[User]:
    try:
        friendship = await repo.get_friends(user_id)
        if friendship is None:
            return []

        sem = Semaphore(5)

        async def fetch(friend_id: str) -> User:
            async with sem:
                return await user_repo.get_user_by_id(friend_id)

        return list(
            await gather(
                *[fetch(i) for i in friendship.friends if i is not None]
            )
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)

async def add_friend(user_id: str, request: FriendDto):
    try:
        return await repo.add_friend(user_id, request.target_user_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)

async def delete_friend(user_id: str, request: FriendDto):
    try:
        return await repo.delete_friend(user_id, request.target_user_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)

async def get_banned_friends(user_id: str) -> list[User]:
    try:

        friendship = await repo.get_friends(user_id)
        if friendship is None:
            return []

        sem = Semaphore(5)

        async def fetch(banned_id: str) -> User:
            async with sem:
                return await user_repo.get_user_by_id(banned_id)

        return list(
            await gather(
                *[fetch(i) for i in friendship.ban if i is not None]
            )
        )

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)

async def ban_friend(user_id: str, request: FriendDto):
    try:
        return await repo.ban_friend(user_id, request.target_user_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)

async def unbanned_friends(user_id: str, request: FriendDto):
    try:
        return await repo.allow_friend(user_id, request.target_user_id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500)