import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from commons.logger import get_marigold_logger
from commons.settings import settings
from databases.mongo_client import init_database
from kafka.topics import KafkaTopic

from models.friendship import Friendship
from models.user import User
from api.user_router import router
from api.friendship_router import friends_router
from consumer.consumer import AuthConsumer

logger = get_marigold_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_task = None
    try:
        await init_database(
            connection_url=settings.MONGO_URL,
            db_name=settings.USER_DB_NAME,
            models=[User, Friendship]
        )

        auth_consumer = AuthConsumer(
            topic=KafkaTopic.USER_AUTH,
            consumer_group="user-service"
        )
        consumer_task = asyncio.create_task(auth_consumer.consume())

    except Exception as e:
        logger.error(f"Failed to start User Service: {e}")
        raise

    yield

    try:
        if consumer_task:
            consumer_task.cancel()
            try:
                await consumer_task
            except asyncio.CancelledError:
                pass
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

app.include_router(router)
app.include_router(friends_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "user"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.USER_INTERNAL_PORT,
        reload=True,
        log_level="info"
    )