def test_ingest_telemetry_returns_201_and_id(client):
    payload = {
        "device_id": "truck-1",
        "lat": 48.137154,
        "lon": 11.576124,
        "battery": 87,
        "timestamp": "2026-01-26T08:00:00Z",
    }

    r = client.post("/api/v1/telemetry", json=payload)
    assert r.status_code == 201

    body = r.json()
    assert "id" in body
    assert body["device_id"] == payload["device_id"]
    assert body["battery"] == payload["battery"]
    assert "ingested_at" in body


def test_state_is_updated_after_ingest(client):
    payload = {
        "device_id": "scooter-9",
        "lat": 48.1,
        "lon": 11.5,
        "battery": 15,
        "timestamp": "2026-01-26T08:00:00Z",
    }

    r1 = client.post("/api/v1/telemetry", json=payload)
    assert r1.status_code == 201
    event_id = r1.json()["id"]

    r2 = client.get(f"/api/v1/state/{payload['device_id']}")
    assert r2.status_code == 200

    state = r2.json()
    assert state["device_id"] == payload["device_id"]
    assert state["battery"] == payload["battery"]
    assert state["last_event_id"] == event_id
