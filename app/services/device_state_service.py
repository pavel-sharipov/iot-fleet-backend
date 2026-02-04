from __future__ import annotations

from app.models.device_state import DeviceStateListOut, DeviceStateOut
from app.repositories.telemetry_repo import TelemetryRepo


class DeviceStateService:
    def __init__(self, repo: TelemetryRepo) -> None:
        self.repo = repo

    @staticmethod
    def _normalize_doc(d: dict) -> dict:
        # копию не делаю: работаем с тем, что пришло из Mongo
        d["id"] = str(d.pop("_id"))
        if "last_event_id" in d and d["last_event_id"] is not None:
            d["last_event_id"] = str(d["last_event_id"])
        return d

    async def near(
        self,
        lat: float,
        lon: float,
        radius_m: int,
        limit: int,
        skip: int,
    ) -> DeviceStateListOut:
        docs = await self.repo.find_states_near(
            lon=lon,
            lat=lat,
            radius_m=radius_m,
            limit=limit,
            skip=skip,
        )

        items = [DeviceStateOut.model_validate(self._normalize_doc(d)) for d in docs]
        return DeviceStateListOut(items=items, limit=limit, skip=skip, count=len(items))

    async def list(
        self,
        *,
        limit: int,
        skip: int,
    ) -> DeviceStateListOut:
        docs = await self.repo.list_states(limit=limit, skip=skip)
        items = [DeviceStateOut.model_validate(self._normalize_doc(d)) for d in docs]
        return DeviceStateListOut(items=items, limit=limit, skip=skip, count=len(items))

    async def low_battery(
        self,
        *,
        lt: int,
        limit: int,
        skip: int,
    ) -> DeviceStateListOut:
        docs = await self.repo.list_low_battery_states(lt=lt, limit=limit, skip=skip)
        items = [DeviceStateOut.model_validate(self._normalize_doc(d)) for d in docs]
        return DeviceStateListOut(items=items, limit=limit, skip=skip, count=len(items))
