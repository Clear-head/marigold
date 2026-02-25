from typing import Any, Dict, Optional


class ChatServiceException(Exception):

    def __init__(
        self,
        message: str = "Chat service error occurred",
        status_code: int = 500,
        error_code: str = "CHAT_ERROR",
        detail: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.detail = detail or {}

    def to_dict(self) -> Dict[str, Any]:
        """예외를 JSON 응답으로 변환"""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "detail": self.detail
        }

    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message}, status_code={self.status_code}, error_code={self.error_code})"