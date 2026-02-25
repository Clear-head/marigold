import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends

from commons.logger import get_marigold_logger
from commons.validate_jwt import JWTValidator
from services.chat_services import ChatService
from services.room_services import RoomService
from websocket.connection_manager import WSConnectionManager
from websocket.handler import WebSocketHandler


logger = get_marigold_logger(__name__)
websocket_router = APIRouter()

jwt_validator = JWTValidator()
connection_manager = WSConnectionManager()
chat_service = ChatService()
room_service = RoomService()


def get_websocket_handler() -> WebSocketHandler:
    """WebSocket 핸들러 의존성 주입"""
    return WebSocketHandler(
        connection_manager=connection_manager,
        chat_service=chat_service,
        room_service=room_service
    )


async def _heartbeat_task(user_id: str, websocket: WebSocket, interval: int = 30) -> None:
    """
    Heartbeat 태스크 (모바일 환경 대응)

    Args:
        user_id: 사용자 ID
        websocket: WebSocket 연결
        interval: Ping 전송 주기 (초)
    """
    try:
        while True:
            await asyncio.sleep(interval)
            await websocket.send_json({
                "type": "ping",
                "timestamp": asyncio.get_event_loop().time()
            })
            logger.debug(f"Ping sent to user {user_id}")
    except Exception as e:
        logger.debug(f"Heartbeat task stopped for user {user_id}: {e}")


@websocket_router.websocket("/ws/chat")
async def chat_websocket(
    websocket: WebSocket,
    handler: WebSocketHandler = Depends(get_websocket_handler)
) -> None:
    # JWT 검증
    try:
        payload = await jwt_validator.verify_jwt_websocket(websocket)
    except Exception as e:
        logger.warning(f"WebSocket authentication failed: {e}")
        return

    user_id = payload["userId"]
    logger.info(f"WebSocket connection attempt from user: {user_id}")
    heartbeat_task = None

    try:
        await connection_manager.connect(user_id, websocket)

        await connection_manager.send_personal_message(
            user_id=user_id,
            message={
                "type": "connection_established",
                "user_id": user_id,
                "message": "Connected to chat server"
            }
        )

        # Heartbeat 태스크 시작 (모바일 재연결 감지)
        heartbeat_task = asyncio.create_task(_heartbeat_task(user_id, websocket))

        while True:
            data = await websocket.receive_json()

            # Pong 응답 처리 (클라이언트가 ping에 응답)
            if data.get("type") == "pong":
                logger.debug(f"Pong received from user {user_id}")
                continue

            logger.debug(f"Message received from {user_id}: {data}")
            await handler.handle_message(user_id, data)

    except WebSocketDisconnect:
        # 클라이언트가 정상적으로 연결을 종료한 경우
        logger.info(f"User {user_id} disconnected normally")

    except Exception as e:
        logger.error(f"Unexpected error for user {user_id}: {e}", exc_info=True)

        # 에러 메시지 전송 시도
        try:
            await connection_manager.send_personal_message(
                user_id=user_id,
                message={
                    "type": "error",
                    "message": "Internal server error"
                }
            )
        except Exception:
            pass  # 이미 연결이 끊겼을 수 있음

    finally:
        # Heartbeat 태스크 취소
        if heartbeat_task:
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass

        await connection_manager.disconnect(user_id)
        logger.info(f"User {user_id} connection cleaned up")
