from fastapi import APIRouter, HTTPException, Depends, Query
from pymongo.database import Database
from starlette import status

from app.db.mongo import get_db
from app.models.device_state import DeviceStateOut, DeviceStateListOut
from app.repositories.telemetry_repo import TelemetryRepo
from app.services.device_state_service import DeviceStateService

router = APIRouter()

@router.get(
    "/state/low-battery",
    status_code=status.HTTP_200_OK,
    tags=["state"],
    response_model=DeviceStateListOut,
    response_model_by_alias=False,
)
def low_battery(
    lt: int = Query(
        20,
        ge=0,
        le=100,
        description="Battery threshold (%). Return devices with battery < lt",
        examples=[20],
    ),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    db: Database = Depends(get_db),
):
    repo = TelemetryRepo(db)

    docs = repo.list_low_battery_states(
        lt= lt,
        limit=limit,
        skip=skip,
    )
    items = [DeviceStateOut.model_validate(d) for d in docs]

    return DeviceStateListOut(
        items=items,
        limit=limit,
        skip=skip,
        count=len(items),
    )

@router.get(
    "/state",
    status_code=status.HTTP_200_OK,
    tags=["state"],
    response_model=DeviceStateListOut,
    response_model_by_alias=False,
)
def list_states(
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    db: Database = Depends(get_db),
):
    repo = TelemetryRepo(db)
    docs = repo.list_states(limit=limit, skip=skip)
    items = [DeviceStateOut.model_validate(d) for d in docs]
    return DeviceStateListOut(items=items, limit=limit, skip=skip, count=len(items))


@router.get("/state/near", response_model=DeviceStateListOut, tags=["state"])
def state_near(
        lat: float = Query(..., ge=-90, le=90),
        lon: float = Query(..., ge=-180, le=180),
        radius_m: int = Query(500, ge=1, le=200_000),
        limit: int = Query(50, ge=1, le=200),
        skip: int = Query(0, ge=0),
        db: Database = Depends(get_db),
):
    repo = TelemetryRepo(db)
    service = DeviceStateService(repo)
    return service.near(lat=lat, lon=lon, radius_m=radius_m, limit=limit, skip=skip)

@router.get(
    "/state/{device_id}",
    status_code=status.HTTP_200_OK,
    tags=["state"],
    response_model=DeviceStateOut,
    response_model_by_alias=False,
)
def get_device_state(
    device_id: str,
    db: Database = Depends(get_db),
):
    repo = TelemetryRepo(db)
    doc = repo.get_state(device_id)

    if doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device state not found",
        )

    return DeviceStateOut.model_validate(doc)



