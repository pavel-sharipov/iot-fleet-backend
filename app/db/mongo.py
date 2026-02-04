import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

_client: AsyncIOMotorClient | None = None


def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise RuntimeError("MONGODB_URI is not set")
        _client = AsyncIOMotorClient(uri)
    return _client

def close_mongo_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None

async def ensure_indexes(db: AsyncIOMotorDatabase) -> None:
    await db.devices_state.create_index([("location", "2dsphere")])


async def get_db() -> AsyncIOMotorDatabase:
    db_name = os.getenv("MONGODB_DB", "iot_fleet")
    return get_mongo_client()[db_name]



