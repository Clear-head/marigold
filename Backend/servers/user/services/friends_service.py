from dto.friends_dto import FriendDto
from commons.logger import get_marigold_logger
from repositories.friends_repository import FriendsRepository

logger = get_marigold_logger(__name__)
repo = FriendsRepository()

async def get_friends(user_id: str):
    try:
        return (await repo.get_friends(user_id)).friends
    except Exception as e:
        logger.error(e)

async def add_friend(user_id: str, request: FriendDto):
    try:
        return await repo.add_friend(user_id, request.target_user_id)
    except Exception as e:
        logger.error(e)

async def delete_friend(user_id: str, request: FriendDto):
    try:
        return await repo.delete_friend(user_id, request.target_user_id)
    except Exception as e:
        logger.error(e)

async def get_banned_friends(user_id: str) -> list[str]:
    try:
        return (await repo.get_friends(user_id)).ban
    except Exception as e:
        logger.error(e)

async def ban_friend(user_id: str, request: FriendDto):
    try:
        return await repo.ban_friend(user_id, request.target_user_id)
    except Exception as e:
        logger.error(e)

async def unbanned_friends(user_id: str, request: FriendDto):
    try:
        return await repo.allow_friend(user_id, request.target_user_id)
    except Exception as e:
        logger.error(e)