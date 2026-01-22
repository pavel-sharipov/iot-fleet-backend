from datetime import datetime, timezone

from app.models.telemetry import TelemetryIn, TelemetryOut
from app.repositories.telemetry_repo import TelemetryRepo


class TelemetryService:
    def __init__(self, repo: TelemetryRepo) -> None:
        self.repo = repo

    def ingest(self, telemetry: TelemetryIn) -> TelemetryOut:

        doc = telemetry.model_dump()
        doc["ingested_at"] = datetime.now(timezone.utc)


        result = self.repo.insert_event(doc)
        event_id = result.inserted_id


        state_doc = {
            "_id": telemetry.device_id,
            "device_id": telemetry.device_id,
            "lat": telemetry.lat,
            "lon": telemetry.lon,
            "battery": telemetry.battery,
            "timestamp": telemetry.timestamp,
            "ingested_at": doc["ingested_at"],
            "last_event_id": event_id,
        }
        self.repo.update_state(telemetry.device_id, state_doc)


        return TelemetryOut.model_validate(
            {
                "_id": event_id,
                **doc,
            }
        )