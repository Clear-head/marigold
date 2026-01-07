from beanie import init_beanie
from pymongo import AsyncMongoClient


async def init_database(connection_url: str, db_name: str, models: str):
    client = AsyncMongoClient(connection_url)
    await init_beanie(
        database=client[db_name],
        document_models=models
    )