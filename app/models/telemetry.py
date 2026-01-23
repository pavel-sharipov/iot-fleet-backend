from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field, field_validator, ConfigDict


class TelemetryIn(BaseModel):
    device_id: str = Field(
        ...,
        description="Unique device identifier",
        json_schema_extra={"example": "truck-42"},
    )

    lat: float = Field(
        ...,
        ge=-90,
        le=90,
        description="Latitude in WGS84",
        json_schema_extra={"example": 48.137154},
    )

    lon: float = Field(
        ...,
        ge=-180,
        le=180,
        description="Longitude in WGS84",
        json_schema_extra={"example": 11.576124},
    )

    battery: int = Field(
        ...,
        ge=0,
        le=100,
        description="Battery level in percent",
        json_schema_extra={"example": 87},
    )

    timestamp: datetime = Field(
        ...,
        description="UTC timestamp when telemetry was generated on device",
        json_schema_extra={"example": "2026-01-21T10:15:30Z"},
    )

class TelemetryOut(TelemetryIn):
    id: str = Field(alias="_id")
    ingested_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @field_validator("id", mode="before")
    @classmethod
    def object_id_to_str(cls, v: Any) -> str:
        return str(v)

class TelemetryListOut(BaseModel):
    items: list[TelemetryOut]
    limit: int
    skip: int
    count: int


