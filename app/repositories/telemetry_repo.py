from pymongo.database import Database
from pymongo.results import InsertOneResult, UpdateResult


class TelemetryRepo:
    def __init__(self, db: Database) -> None  :
        self.events = db["telemetry"]
        self.state = db["vehicles_state"]

    def insert_event(self, doc: dict) -> InsertOneResult :
        return self.events.insert_one(doc)

    def update_state(self, device_id: str, state_doc: dict) -> UpdateResult:
        return self.state.update_one(
            {"_id": device_id},
            {"$set": state_doc},
            upsert=True,
            )

    def get_state(self, device_id: str):
        return self.state.find_one({"_id": device_id})

