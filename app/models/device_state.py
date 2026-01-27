from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.models.geo import GeoPoint


class DeviceStateOut(BaseModel):
    id: str = Field(alias="_id")
    device_id: str
    lat: float
    lon: float
    battery: int
    timestamp: datetime
    ingested_at: datetime
    last_event_id: str
    location: Optional[GeoPoint] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("id", mode="before")
    @classmethod
    def _id_to_str(cls, v: Any) -> str:
        return str(v)

    @field_validator("last_event_id", mode="before")
    @classmethod
    def last_event_id_to_str(cls, v: Any) -> str:
        return str(v)

class DeviceStateListOut(BaseModel):
    items: list[DeviceStateOut]
    limit: int
    skip: int
    count: int