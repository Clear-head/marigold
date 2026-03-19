from beanie.odm.operators.update.array import AddToSet, Pull
from commons.logger import get_marigold_logger
from models.friendship import Friendship



class FriendsRepository:
    def __init__(self):
        self.logger = get_marigold_logger(__name__)


    async def create_friends(self, new_friendship: Friendship) -> Friendship:
        try:
            return await new_friendship.save()
        except Exception as e:
            self.logger.error(f"from repository: {e}")

    async def get_friends(self, user_id: str) -> Friendship:
        try:
            return await Friendship.find_one(Friendship.user_id==user_id)
        except Exception as e:
            self.logger.error(f"from repository: {e}")

    async def add_friend(self, user_id: str, new_friends_id: str):
        try:
            await Friendship.find_one(Friendship.user_id == user_id).update(
                AddToSet({"friends": new_friends_id})
            )
            return True
        except Exception as e:
            self.logger.error(f"from repository: {e}")
            return False

    async def delete_friend(self, user_id: str, target_user_id: str):
        try:
            await Friendship.find_one(Friendship.user_id == user_id).update(
                Pull({"friends": target_user_id})
            )
        except Exception as e:
            self.logger.error(f"from repository: {e}")

    async def ban_friend(self, user_id: str, target_user_id: str):
        try:
            await Friendship.find_one(Friendship.user_id == user_id).update(
                AddToSet({"ban": target_user_id})
            )
        except Exception as e:
            self.logger.error(f"from repository: {e}")

    async def allow_friend(self, user_id: str, target_user_id: str):
        try:
            await Friendship.find_one(Friendship.user_id == user_id).update(
                Pull({"ban": target_user_id})
            )
        except Exception as e:
            self.logger.error(f"from repository: {e}")
