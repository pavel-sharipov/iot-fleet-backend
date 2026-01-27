from typing import Literal
from pydantic import BaseModel, Field

class GeoPoint(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: list[float] = Field(..., min_length=2, max_length=2)  # [lon, lat]