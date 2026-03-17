from chat_exceptions.base import ChatServiceException
from chat_exceptions.room_exceptions import (
    RoomNotFoundException,
    RoomAccessDeniedException,
    UserAlreadyInRoomException,
    UserNotInRoomException,
    EmptyRoomException
)
from chat_exceptions.message_exceptions import (
    MessageNotFoundException,
    InvalidMessageTypeException,
    MessageSendFailedException
)

__all__ = [
    # Base
    "ChatServiceException",

    # Room Exceptions
    "RoomNotFoundException",
    "RoomAccessDeniedException",
    "UserAlreadyInRoomException",
    "UserNotInRoomException",
    "EmptyRoomException",

    # Message Exceptions
    "MessageNotFoundException",
    "InvalidMessageTypeException",
    "MessageSendFailedException",
]