from typing import Any, Dict, Optional
from chat_exceptions.base import ChatServiceException


class MessageNotFoundException(ChatServiceException):
    """메시지를 찾을 수 없을 때 발생하는 예외"""

    def __init__(
        self,
        message_id: str,
        detail: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"메시지를 찾을 수 없습니다. (message_id: {message_id})",
            status_code=404,
            error_code="MESSAGE_NOT_FOUND",
            detail=detail or {"message_id": message_id}
        )


class InvalidMessageTypeException(ChatServiceException):
    """잘못된 메시지 타입일 때 발생하는 예외"""

    def __init__(
        self,
        message_type: str,
        detail: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"지원하지 않는 메시지 타입입니다. (type: {message_type})",
            status_code=400,
            error_code="INVALID_MESSAGE_TYPE",
            detail=detail or {"message_type": message_type}
        )


class MessageSendFailedException(ChatServiceException):
    """메시지 전송 실패 시 발생하는 예외"""

    def __init__(
        self,
        reason: str,
        detail: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"메시지 전송에 실패했습니다. ({reason})",
            status_code=500,
            error_code="MESSAGE_SEND_FAILED",
            detail=detail or {"reason": reason}
        )