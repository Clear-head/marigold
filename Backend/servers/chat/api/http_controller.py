from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Header, Query, Path, status

from commons.validate_jwt import JWTValidator
from starlette.responses import JSONResponse

from services.chat_services import ChatService
from services.room_services import RoomService
from dto.chat_room_dto import CreateChatRoomDto, InviteChatRoomDto, ExitChatRoomDto


router = APIRouter(prefix="/api/chat", tags=["Chat"])

jwt_validator = JWTValidator()
chat_service = ChatService()
room_service = RoomService()


@router.get("/rooms", status_code=status.HTTP_200_OK)
async def get_my_rooms(authorization: Annotated[str, Header()]):
    """내가 속한 채팅방 목록 조회"""
    # JWT 검증 및 사용자 ID 추출
    payload = await jwt_validator.verify_jwt_http(authorization)
    user_id = payload["userId"]

    result = await room_service.get_rooms(user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=result.model_dump(mode='json')
    )



@router.post("/rooms", status_code=status.HTTP_201_CREATED)
async def create_room(
        authorization: Annotated[str, Header()],
        request: CreateChatRoomDto,
):
    # JWT 검증 및 사용자 ID 추출
    payload = await jwt_validator.verify_jwt_http(authorization)
    user_id = payload["userId"]

    # 채팅방 생성
    room_id = await room_service.create_chat_room(request)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"room_id": room_id}
    )



@router.delete("/rooms", status_code=status.HTTP_204_NO_CONTENT)
async def exit_room(
    authorization: Annotated[str, Header()],
    request: ExitChatRoomDto
):
    """채팅방 나가기"""
    # JWT 검증
    payload = await jwt_validator.verify_jwt_http(authorization)
    user_id = payload["userId"]

    # 채팅방 나가기
    await room_service.exit_chat_room(request)
    return JSONResponse(status_code=status.HTTP_200_OK, content=None)


@router.post("/rooms/{room_id}/members", status_code=status.HTTP_200_OK)
async def invite_member(authorization: Annotated[str, Header()], request: InviteChatRoomDto):
    """채팅방에 맴버 초대"""
    # JWT 검증
    payload = await jwt_validator.verify_jwt_http(authorization)
    sender_id = payload["userId"]

    await room_service.invite_user_to_room(request)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=None
    )



@router.get("/rooms/{room_id}/messages", status_code=status.HTTP_200_OK)
async def get_message_history(
    authorization: Annotated[str, Header()],
    room_id: Annotated[str, Path()],
    last_message_id: Annotated[Optional[str], Query()] = None
):
    """
    채팅방 메시지 히스토리 조회
    """
    # JWT 검증
    payload = await jwt_validator.verify_jwt_http(authorization)
    user_id = payload["userId"]

    msgs = await chat_service.get_messages(room_id, last_message_id)

    # Beanie Document를 dict로 변환
    msgs_dict = [msg.model_dump(mode='json') for msg in msgs]

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"messages": msgs_dict}
    )