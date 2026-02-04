from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from pathlib import Path

from app.api.v1.router import api_router
from app.db.mongo import get_db, ensure_indexes, close_mongo_client

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = await get_db()
    await ensure_indexes(db)
    yield
    close_mongo_client()


app = FastAPI(
    title="IoT Fleet Backend",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api/v1")