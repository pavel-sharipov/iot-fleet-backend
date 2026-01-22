from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo.database import Database
from starlette import status
from bson import ObjectId
from app.db.mongo import get_db
from app.models.telemetry import TelemetryIn, TelemetryOut, TelemetryListOut

from app.repositories.telemetry_repo import TelemetryRepo
from app.services.telemetry_service import TelemetryService

router = APIRouter()

COLLECTION_NAME = "telemetry"


@router.post("/telemetry",
    status_code=status.HTTP_201_CREATED,
    tags=["telemetry"],
    response_model=TelemetryOut,
    response_model_by_alias=False
)
def ingest_telemetry(
        telemetry: TelemetryIn,
        db: Database = Depends(get_db),
):
    # doc = telemetry.model_dump()
    # doc["ingested_at"] = datetime.now(timezone.utc)
    #
    # collection = db[COLLECTION_NAME]
    # try:
    #     result = collection.insert_one(doc)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=str(e),
    #     )
    # saved = collection.find_one({"_id": result.inserted_id})
    # if saved is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail="Inserted document not found",
    #     )
    # return TelemetryOut.model_validate(saved)
    repo = TelemetryRepo(db)
    service = TelemetryService(repo)
    return service.ingest(telemetry)

@router.get(
    "/telemetry/{telemetry_id}",
    status_code=status.HTTP_200_OK,
    tags=["telemetry"],
    response_model=TelemetryOut,
    response_model_by_alias=False
)
def get_telemetry(
    telemetry_id: str,
    db: Database = Depends(get_db),
):
    collection = db[COLLECTION_NAME]

    if not ObjectId.is_valid(telemetry_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid telemetry_id",
        )

    obj_id = ObjectId(telemetry_id)

    doc = collection.find_one({"_id": obj_id})
    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Telemetry not found",
        )

    return TelemetryOut.model_validate(doc)

@router.get("/telemetry",
    status_code=status.HTTP_200_OK,
    tags=["telemetry"],
    response_model=TelemetryListOut,
    response_model_by_alias=False
)
def list_telemetry(
        limit: int = Query(50, ge=1, le=200),
        skip: int = Query(0, ge=0),
        db: Database = Depends(get_db),
):
    collection = db[COLLECTION_NAME]
    try:
        cursor = (
            collection.find({})
            .sort("_id", -1)
            .skip(skip)
            .limit(limit)
        )
        docs = list(cursor)
        items = [TelemetryOut.model_validate(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return {
        "items": items,
        "limit": limit,
        "skip": skip,
        "count" : len(items),
    }