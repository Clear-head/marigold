import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class RootSettings(BaseSettings):
    MONGO_URL: str

    AUTH_DB_NAME: str
    CHAT_DB_NAME: str
    AI_DB_NAME: str
    CALENDAR_DB_NAME: str

    KAFKA_BOOTSTRAP_SERVERS: str
    REDIS_URL: str

    OLLAMA_BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../infrastructure/.env"),
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = RootSettings()