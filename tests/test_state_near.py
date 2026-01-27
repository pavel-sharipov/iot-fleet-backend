import os
import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_MONGO_INTEGRATION") != "1",
    reason="Geo queries ($near/2dsphere) require real MongoDB (mongomock does not support it reliably).",
)

def test_state_near_finds_device(client):
    payload = {
        "device_id": "scooter-9",
        "timestamp": "2026-01-26T08:00:00Z",
        "lat": 48.137154,
        "lon": 11.576124,
        "battery": 80,
        "status": "ok",
    }
    r = client.post("/api/v1/telemetry", json=payload)
    assert r.status_code in (200, 201), r.text

    r2 = client.get("/api/v1/state/near", params={"lat": 48.137154, "lon": 11.576124, "radius_m": 1000})
    assert r2.status_code == 200, r2.text
    data = r2.json()
    assert any(x["device_id"] == "scooter-9" for x in data["items"])
