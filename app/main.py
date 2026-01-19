import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pymongo.server_api import ServerApi

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI()

@app.get("/db-ping")
def db_ping():
    uri = os.getenv("MONGODB_URI")
    if not uri:
        raise HTTPException(status_code=500, detail="MONGODB_URI is not set")

    try:
        client = MongoClient(uri, server_api=ServerApi("1"))
        client.admin.command("ping")
        return {"mongodb": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
