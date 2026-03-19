from typing import Annotated

from fastapi import APIRouter, Header
from commons.validate_jwt import JWTValidator
from services.friends_service import add_friend, get_friends, delete_friend, ban_friend, unbanned_friends, get_banned_friends
from dto.friends_dto import FriendDto

friends_router = APIRouter(
    prefix = "/user",
    tags = ["Friendship"],
)

jwt_validator = JWTValidator()

@router.get("/friends")
async def get_friend(authorization: Annotated[str, Header()]):
    user_id = (await jwt_validator.verify_jwt_http(authorization))["userId"]
    return await get_friends(user_id=user_id)


@router.post("/friends")
async def add_friends(request: FriendDto, authorization: Annotated[str, Header()]):
    user_id = (await jwt_validator.verify_jwt_http(authorization))["userId"]
    return await add_friend(user_id = user_id, request=request)


@router.delete("/friends")
async def delete_friends(request: FriendDto, authorization: Annotated[str, Header()]):
    user_id = (await jwt_validator.verify_jwt_http(authorization))["userId"]
    return await delete_friend(user_id = user_id, request=request)





@router.get("/blocks")
async def get_banned_users(authorization: Annotated[str, Header()]):
    user_id = (await jwt_validator.verify_jwt_http(authorization))["userId"]
    return await get_banned_friends(user_id=user_id)


@router.post("/blocks")
async def ban_users(request: FriendDto, authorization: Annotated[str, Header()]):
    user_id = (await jwt_validator.verify_jwt_http(authorization))["userId"]
    return await ban_friend(user_id = user_id, request=request)


@router.delete("/blocks")
async def allow_users(request: FriendDto, authorization: Annotated[str, Header()]):
    user_id = (await jwt_validator.verify_jwt_http(authorization))["userId"]
    return await unbanned_friends(user_id = user_id, request=request)
