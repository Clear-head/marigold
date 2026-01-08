import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class RootSettings(BaseSettings):
    # MongoDB
    MONGO_URL: str

    AUTH_DB_NAME: str
    CHAT_DB_NAME: str
    AI_DB_NAME: str
    CALENDAR_DB_NAME: str

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str

    # Redis
    REDIS_URL: str

    # Ollama
    OLLAMA_BASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ISSUER: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    MAX_DEVICES_PER_USER: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../infrastructure/.env"),
        env_file_encoding='utf-8',
        extra='ignore'
    )


settings = RootSettings()