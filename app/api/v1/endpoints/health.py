from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.mongo import get_db, get_mongo_client

router = APIRouter()


@router.get("/health")
def health():
    return {"ok": True}


@router.get("/db-ping")
async def db_ping():
    try:
        client = get_mongo_client()
        await client.admin.command("ping")
        return {"mongodb": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/db-name")
async def db_name(db: AsyncIOMotorDatabase = Depends(get_db)):
    return {"db": db.name}
