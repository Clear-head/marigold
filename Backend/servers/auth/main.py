import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from commons.logger import get_marigold_logger
from commons.settings import settings
from databases.mongo_client import init_database
from databases.redis_client import get_redis_client, close_redis_client
from kafka.producer import kafka_producer
from models.credential import UserCredential
from api.auth_router import router
from handler.exception_handler import auth_exception_handler, general_exception_handler
from exceptions.auth_exceptions import AuthException

logger = get_marigold_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_database(
            connection_url=settings.MONGO_URL,
            db_name=settings.AUTH_DB_NAME,
            models=[UserCredential]
        )
        await get_redis_client()
        await kafka_producer.init_producer()

    except Exception as e:
        logger.error(f"Failed to start Auth Service: {e}")
        raise

    yield

    try:
        await kafka_producer.close()
        await close_redis_client()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(AuthException, auth_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "auth"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.AUTH_INTERNAL_PORT,
        reload=True,
        log_level="info"
    )