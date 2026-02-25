import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from commons.logger import get_marigold_logger
from commons.settings import settings
from databases.mongo_client import init_database
from databases.redis_client import get_redis_client, close_redis_client
from kafka.producer import kafka_producer
from kafka.topics import KafkaTopic
from kafka_consumer.from_user_consumer import UserConsumer
from models.chat_room import ChatRoom
from models.messages import TextMessage, ImageMessage, VideoMessage
from api.http_controller import router as http_router
from websocket.router import websocket_router
from exceptions.base import ChatServiceException

logger = get_marigold_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = None
    try:
        await init_database(
            connection_url=settings.MONGO_URL,
            db_name=settings.CHAT_DB_NAME,
            models=[ChatRoom, TextMessage, ImageMessage, VideoMessage]
        )
        await get_redis_client()
        await kafka_producer.init_producer()

        user_consumer = UserConsumer(
            topic=KafkaTopic.USER_PROFILE,
            consumer_group="chat-service"
        )
        consumer_task = asyncio.create_task(user_consumer.consume())

    except Exception as e:
        logger.error(f"Failed to start Chat Service: {e}")
        raise

    yield

    try:
        if consumer_task:
            consumer_task.cancel()
            try:
                await consumer_task
            except asyncio.CancelledError:
                pass
        await kafka_producer.close()
        await close_redis_client()

    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

app = FastAPI(lifespan=lifespan)


# 예외 핸들러 등록
@app.exception_handler(ChatServiceException)
async def chat_service_exception_handler(request: Request, exc: ChatServiceException):
    """Chat 서비스 예외 처리"""
    logger.warning(f"ChatServiceException: {exc.error_code} - {exc.message}", extra={"detail": exc.detail})
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(http_router)

app.include_router(websocket_router)


@app.get("/health", tags=["Health"])
async def health_check():
    """서비스 상태 확인 엔드포인트"""
    return {
        "status": "healthy",
        "service": "chat"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )