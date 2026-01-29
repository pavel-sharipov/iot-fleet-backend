from app.models.device_state import DeviceStateListOut, DeviceStateOut
from app.repositories.telemetry_repo import TelemetryRepo


class DeviceStateService:
    def __init__(self, repo: TelemetryRepo) -> None:
        self.repo = repo

    def near(
        self,
        lat: float,
        lon: float,
        radius_m: int,
        limit: int,
        skip: int,
    ) -> DeviceStateListOut:
        docs = self.repo.find_states_near(
            lon=lon,
            lat=lat,
            radius_m=radius_m,
            limit=limit,
            skip=skip,
        )

        items = []
        for d in docs:
            d["id"] = str(d.pop("_id"))
            if "last_event_id" in d and d["last_event_id"] is not None:
                d["last_event_id"] = str(d["last_event_id"])
            items.append(DeviceStateOut.model_validate(d))

        return DeviceStateListOut(
            items=items,
            limit=limit,
            skip=skip,
            count=len(items),
        )
    def list(
        self,
        *,
        limit: int,
        skip: int,
    ) -> DeviceStateListOut:
        docs = self.repo.list_states(limit=limit, skip=skip)
        items = [DeviceStateOut.model_validate(d) for d in docs]
        return DeviceStateListOut(items=items, limit=limit, skip=skip, count=len(items))

    def low_battery(
        self,
        *,
        lt: int,
        limit: int,
        skip: int,
    ) -> DeviceStateListOut:
        docs = self.repo.list_low_battery_states(
            lt=lt,
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