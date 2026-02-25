from asyncio import gather
from typing import Dict, Any

from commons.logger import get_marigold_logger
from starlette.websockets import WebSocket, WebSocketDisconnect

from dto.message_dto import MessageDTO
from models.messages import BaseMessage


class WSConnectionManager:
    """WebSocket 연결 관리자"""

    def __init__(self):
        self.logger = get_marigold_logger(__name__)
        self.activate_users: Dict[str, WebSocket] = {}


    async def connect(self, user_id: str, websocket: WebSocket) -> None:

        try:
            await websocket.accept()
            self.activate_users[user_id] = websocket
            self.logger.info(f"User {user_id} connected (total: {len(self.activate_users)})")
        except Exception as e:
            self.logger.error(f"Failed to connect user {user_id}: {e}")
            raise


    async def disconnect(self, user_id: str) -> None:

        try:
            # WebSocket 객체 가져오기
            websocket = self.activate_users.get(user_id)

            # 활성 연결에서 제거
            if user_id in self.activate_users:
                del self.activate_users[user_id]

            # WebSocket 닫기
            if websocket:
                try:
                    await websocket.close()
                except Exception:
                    pass  # 이미 닫혀있을 수 있음

            self.logger.info(f"User {user_id} disconnected (total: {len(self.activate_users)})")

        except Exception as e:
            self.logger.error(f"Error disconnecting user {user_id}: {e}")


    async def send_personal_message(self, user_id: str, message: dict) -> None:

        try:
            if user_id in self.activate_users:
                websocket = self.activate_users[user_id]
                await websocket.send_json(message)
                self.logger.debug(f"Sent personal message to {user_id}")

            else:
                self.logger.warning(f"User {user_id} is not connected")

        except WebSocketDisconnect:
            self.logger.warning(f"User {user_id} disconnected while sending message")
            await self.disconnect(user_id)

        except Exception as e:
            self.logger.error(f"Failed to send message to {user_id}: {e}")
            await self.disconnect(user_id)

    async def broadcast_to_users(self, user_ids: list[str], message: BaseMessage) -> list[Any] | None:
        try:
            sent_count = 0
            failed_users = []
            offline_users = []

            for user_id in user_ids:
                # 온라인 사용자에게만 전송
                if user_id in self.activate_users:
                    try:
                        websocket = self.activate_users[user_id]
                        await websocket.send_json(message.model_dump(mode='json'))
                        sent_count += 1

                    except WebSocketDisconnect:
                        self.logger.warning(f"User {user_id} disconnected during broadcast")
                        failed_users.append(user_id)

                    except Exception as e:
                        self.logger.error(f"Failed to send to {user_id}: {e}")
                        failed_users.append(user_id)
                else:
                    #   오프라인 유저 추가
                    offline_users.append(user_id)

            # 실패한 연결 정리
            await gather(
                *[self.disconnect(i) for i in failed_users]
            )

            offline_users.extend(failed_users)

            self.logger.info(f"Broadcast to {sent_count}/{len(user_ids)} online users")

            return offline_users

        except Exception as e:
            self.logger.error(f"Error broadcasting to users: {e}")

    def is_user_online(self, user_id: str) -> bool:
        """사용자 온라인 상태 확인"""
        return user_id in self.activate_users

    def get_connection_count(self) -> int:
        """현재 연결된 사용자 수 반환"""
        return len(self.activate_users)