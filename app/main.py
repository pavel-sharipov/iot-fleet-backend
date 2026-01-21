from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path

from app.api.v1.router import api_router

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

app = FastAPI(title="IoT Fleet Backend")

app.include_router(api_router, prefix="/api/v1")
