import asyncio
import json
from contextlib import asynccontextmanager

import firebase_admin
import uvicorn
from fastapi import FastAPI
from firebase_admin import credentials
from starlette.middleware.cors import CORSMiddleware

from api.notification_router import router as notification_router
from commons.logger import get_marigold_logger
from commons.settings import settings
from databases.mongo_client import init_database
from databases.redis_client import close_redis_client
from exceptions.notification_exceptions import NotificationException
from handler.exception_handler import notification_exception_handler, general_exception_handler
from kafka.topics import KafkaTopic
from kafka_consumer.from_auth_consumer import UserConsumer
from kafka_consumer.from_chat_consumer import ChatConsumer
from models.firebase_token import FCM

logger = get_marigold_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_tasks = []
    try:
        await init_database(
            connection_url=settings.MONGO_URL,
            db_name=settings.NOTIFICATION_DB_NAME,
            models=[FCM]
        )
        cred = credentials.Certificate(json.loads(settings.FIREBASE_CREDENTIALS_JSON))
        firebase_admin.initialize_app(cred)

        chat_consumer = ChatConsumer(
            topic=KafkaTopic.NOTIFICATION_PUSH,
            consumer_group="notification-service"
        )
        user_consumer = UserConsumer(
            topic=KafkaTopic.USER_AUTH,
            consumer_group="notification-service"
        )
        consumer_tasks.append(asyncio.create_task(chat_consumer.consume()))
        consumer_tasks.append(asyncio.create_task(user_consumer.consume()))

    except Exception as e:
        logger.error(f"Failed to start Notification Service: {e}")
        raise

    yield

    try:
        for task in consumer_tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        firebase_admin.delete_app(firebase_admin.get_app())
        await close_redis_client()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notification_router)
app.add_exception_handler(NotificationException, notification_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "notification"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.NOTIFICATION_INTERNAL_PORT,
        reload=True,
        log_level="info"
    )
