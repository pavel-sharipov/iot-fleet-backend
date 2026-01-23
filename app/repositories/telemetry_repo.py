from typing import Any, Optional

from bson import ObjectId

from pymongo.database import Database


class TelemetryRepo:
    EVENTS_COLLECTION = "telemetry"
    STATE_COLLECTION = "devices_state"

    def __init__(self, db: Database) -> None:
        self.events = db[self.EVENTS_COLLECTION]
        self.state = db[self.STATE_COLLECTION]
    # events
    def insert_event(self, doc: dict):
        return self.events.insert_one(doc)

    def get_event_by_id(self, obj_id: ObjectId) -> dict | None:
        return self.events.find_one({"_id": obj_id})

    def list_events(self, limit: int, skip: int) -> list[dict]:
        cursor = (
            self.events.find({})
            .sort("_id", -1)
            .skip(skip)
            .limit(limit)
        )
        return list(cursor)

    # state
    def update_state(self, device_id: str, state_doc: dict):
        return self.state.update_one(
            {"_id": device_id},
            {"$set": state_doc},
            upsert=True,
        )

    def get_state(self, device_id: str) -> dict | None:
        return self.state.find_one({"_id": device_id})

    def list_states(
            self,
            limit: int,
            skip: int,
            query: Optional[dict] = None,
            sort: Optional[list[tuple[str, int]]] = None,
    ) -> list[dict]:
        q = query or {}
        s = sort or [("ingested_at", -1)]

        cursor = (
            self.state.find(q)
            .sort(s)
            .skip(skip)
            .limit(limit)
        )
        return list(cursor)

    def list_low_battery_states(self, lt: int, limit: int, skip: int) -> list[dict]:
        return self.list_states(
            limit=limit,
            skip=skip,
            query={"battery": {"$lt": lt}},
            sort=[("battery", 1), ("ingested_at", -1)],
        )