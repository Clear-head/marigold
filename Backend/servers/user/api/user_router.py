# Backend\servers\user\api\user_router.py
# fastapi

from fastapi import APIRouter, status, Header, Depends, HTTPException
from typing import Annotated

from services.user_service import UserService
from dto.change_name_dto import RequestChangeName, ResponseChangeName
from dto.change_phone_dto import RequestChangePhone, ResponseChangePhone
from dto.change_birth_dto import RequestChangeBirth, ResponseChangeBirth
from dto.read_user_dto import RequestUserInfoDTO, ResponseUserInfoDTO
from commons.validate_jwt import JWTValidator

router = APIRouter(
    prefix = "/user",
    tags = ["User"]
)

jwt_validator = JWTValidator()
user_service = UserService()

@router.post("/name", response_model = ResponseChangeName, status_code = status.HTTP_202_ACCEPTED)
async def change_name_endpoint(
    request: RequestChangeName, 
    authorization: Annotated[str, Header()]
):
    payload = await jwt_validator.verify_jwt_http(authorization)
    user_id = payload["userId"]
    
    return await user_service.change_name(name_info=request, user_id=user_id)

@router.post("/phone", response_model = ResponseChangePhone, status_code = status.HTTP_202_ACCEPTED)
async def change_phone_endpoint(
    request: RequestChangePhone,
    authorization: Annotated[str, Header()]
):
    payload = await jwt_validator.verify_jwt_http(authorization)
    user_id = payload["userId"]

    return await user_service.change_phone(phone_info=request, user_id=user_id)

@router.post("/birth", response_model = ResponseChangeBirth, status_code = status.HTTP_202_ACCEPTED)
async def change_birth_endpoint(
    request: RequestChangeBirth,
    authorization: Annotated[str, Header()]
):
    payload = await jwt_validator.verify_jwt_http(authorization)
    user_id = payload["userId"]

    return await user_service.change_birth(birth_info=request, user_id=user_id)


@router.get("/", response_model=list[ResponseUserInfoDTO])
async def get_user_info(
    authorization: Annotated[str, Header()],
    request: Annotated[RequestUserInfoDTO, Depends()]
):
    await jwt_validator.verify_jwt_http(authorization)
    return await user_service.get_user_info(request)
