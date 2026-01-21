from fastapi import APIRouter
from app.api.v1.endpoints import health
from app.api.v1.endpoints import telemetry

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(telemetry.router, tags=["telemetry"])