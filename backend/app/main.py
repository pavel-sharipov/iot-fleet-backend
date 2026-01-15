import os
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI(title="IoT Fleet Telemetry API")

def get_db():
    uri = os.environ["MONGODB_URI"]
    client = MongoClient(uri)
    return client

@app.get("/health")
def health():
    # healthcheck
    return {"status": "ok"}

@app.get("/db-ping")
def db_ping():
    client = get_db()
    client.admin.command("ping")
    return {"mongodb": "ok"}
