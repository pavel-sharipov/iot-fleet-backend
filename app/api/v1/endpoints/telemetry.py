from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from starlette import status
from fastapi import HTTPException

from app.db.mongo import get_db
from app.models.telemetry import TelemetryIn

router = APIRouter()

COLLECTION_NAME = "telemetry"

@router.post("/telemetry", status_code=status.HTTP_201_CREATED, tags=["telemetry"])
def ingest_telemetry(
        telemetry: TelemetryIn,
        db: Database = Depends(get_db),
):
    doc = telemetry.model_dump()

    collection = db[COLLECTION_NAME]
    try:
        result = collection.insert_one(doc)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {"status": "stored", "id" : str(result.inserted_id)}
