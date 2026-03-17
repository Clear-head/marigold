from typing import Any, Dict, Optional
from chat_exceptions.base import ChatServiceException


class RoomNotFoundException(ChatServiceException):
    """채팅방을 찾을 수 없을 때 발생하는 예외"""

    def __init__(
        self,
        room_id: str,
        detail: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"채팅방을 찾을 수 없습니다. (room_id: {room_id})",
            status_code=404,
            error_code="ROOM_NOT_FOUND",
            detail=detail or {"room_id": room_id}
        )


class RoomAccessDeniedException(ChatServiceException):
    """채팅방 접근 권한이 없을 때 발생하는 예외"""

    def __init__(
        self,
        room_id: str,
        user_id: str,
        detail: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message="해당 채팅방에 접근할 권한이 없습니다.",
            status_code=403,
            error_code="ROOM_ACCESS_DENIED",
            detail=detail or {"room_id": room_id, "user_id": user_id}
        )


class UserAlreadyInRoomException(ChatServiceException):
    """사용자가 이미 채팅방에 있을 때 발생하는 예외"""

    def __init__(
        self,
        room_id: str,
        user_id: str,
        detail: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message="이미 채팅방에 참여 중인 사용자입니다.",
            status_code=409,
            error_code="USER_ALREADY_IN_ROOM",
            detail=detail or {"room_id": room_id, "user_id": user_id}
        )


class UserNotInRoomException(ChatServiceException):
    """사용자가 채팅방에 없을 때 발생하는 예외"""

    def __init__(
        self,
        room_id: str,
        user_id: str,
        detail: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message="채팅방에 참여 중이지 않은 사용자입니다.",
            status_code=404,
            error_code="USER_NOT_IN_ROOM",
            detail=detail or {"room_id": room_id, "user_id": user_id}
        )


class EmptyRoomException(ChatServiceException):
    """채팅방이 비어있을 때 발생하는 예외"""

    def __init__(
        self,
        room_id: str,
        detail: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message="채팅방에 참여자가 없습니다.",
            status_code=400,
            error_code="EMPTY_ROOM",
            detail=detail or {"room_id": room_id}
        )