from datetime import datetime, timezone
from pydantic import BaseModel, Field


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
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when telemetry was generated",
        json_schema_extra={"example": "2026-01-21T10:15:30Z"},
    )
