from exceptions.base import ChatServiceException
from exceptions.room_exceptions import (
    RoomNotFoundException,
    RoomAccessDeniedException,
    UserAlreadyInRoomException,
    UserNotInRoomException,
    EmptyRoomException
)
from exceptions.message_exceptions import (
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