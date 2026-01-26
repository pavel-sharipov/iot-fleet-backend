import os
import uuid

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.main import app
import app.db.mongo as mongo_mod


@pytest.fixture(scope="session")
def test_db_name() -> str:
    return f"iot_fleet_test_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="session")
def mongo_client() -> MongoClient:
    uri = os.getenv("MONGODB_URI", "mongodb://mongo:27017")
    return MongoClient(uri)


@pytest.fixture(scope="session")
def client(test_db_name: str):
    os.environ["MONGODB_URI"] = os.getenv("MONGODB_URI", "mongodb://mongo:27017")
    os.environ["MONGODB_DB"] = test_db_name

    mongo_mod._client = None

    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_db(mongo_client: MongoClient, test_db_name: str):
    db = mongo_client[test_db_name]
    db["telemetry"].delete_many({})
    db["devices_state"].delete_many({})
    yield


@pytest.fixture(scope="session", autouse=True)
def drop_test_db(mongo_client: MongoClient, test_db_name: str):
    yield
    mongo_client.drop_database(test_db_name)
