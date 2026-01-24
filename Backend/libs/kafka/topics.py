from enum import Enum


class KafkaTopic(str, Enum):
    """
    Kafka 토픽 정의 - marigold.서비스.도메인 형식

    네이밍 규칙:
    - prefix: marigold (프로젝트명)
    - service: chat, user, notification, calendar 등
    - domain: message, room, auth, profile 등
    """

    # Chat Service
    CHAT_MESSAGE = "marigold.chat.message"
    CHAT_ROOM = "marigold.chat.room"

    # User Service
    USER_AUTH = "marigold.user.auth"
    USER_PROFILE = "marigold.user.profile"

    # Notification Service
    NOTIFICATION_PUSH = "marigold.notification.push"

    # Calendar Service
    CALENDAR_EVENT = "marigold.calendar.event"