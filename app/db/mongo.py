import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database

_client: MongoClient | None = None


def get_mongo_client() -> MongoClient:
    global _client

    if _client is None:
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise RuntimeError("MONGODB_URI is not set")

        _client = MongoClient(uri, server_api=ServerApi("1"))

    return _client

def ensure_indexes(db: Database) -> None:
    db.devices_state.create_index([("location", "2dsphere")])

def get_db() -> Database:
    db_name = os.getenv("MONGODB_DB", "iot_fleet")
    return get_mongo_client()[db_name]


