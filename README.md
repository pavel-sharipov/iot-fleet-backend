[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

# IoT Fleet Telemetry Backend

Ein modernes Backend zur Verarbeitung, Speicherung und Auswertung von Telemetriedaten aus einer IoT-Fahrzeugflotte.

Die Anwendung bildet ein realistisches Szenario ab: Geräte wie E-Scooter, Lieferfahrzeuge oder Sensoren senden regelmäßig Positions- und Batteriedaten an ein FastAPI-Backend. Eingehende Daten werden validiert, in MongoDB gespeichert und zusätzlich in ein separates Zustandsmodell überführt, damit der **aktuelle Gerätezustand** schnell und effizient abgefragt werden kann.

Das Projekt ist bewusst als **portfolio-taugliches Backend-Projekt** aufgebaut und zeigt praxisnahe Kenntnisse in den Bereichen:

---

## Funktionen

- REST-API-Entwicklung mit FastAPI
- asynchrone Backend-Programmierung
- Datenmodellierung mit MongoDB
- Geo-Abfragen mit `2dsphere`
- Docker-basierte Entwicklungs- und Deployment-Umgebung
- saubere Schichtenarchitektur
- automatisierte Tests mit `pytest`

---
## Projektüberblick

In vielen IoT- und Fleet-Management-Systemen gibt es zwei unterschiedliche Anforderungen:

1. **fortlaufende Speicherung aller eingehenden Rohdaten**
2. **schnelle Abfragen des zuletzt bekannten Zustands eines Geräts**

Dieses Projekt trennt diese beiden Anwendungsfälle bewusst:

- Alle eingehenden Ereignisse werden in der Collection `telemetry` gespeichert.
- Der letzte bekannte Zustand je Gerät wird in `devices_state` gehalten.

Dadurch entsteht ein realistischer Ansatz, wie er auch in produktionsnahen Backend-Systemen verwendet wird: historische Rohdaten bleiben erhalten, während aktuelle Zustandsabfragen performant bleiben.

---
## Funktionsumfang

- Entgegennahme von Telemetriedaten per REST-API
- Validierung eingehender JSON-Payloads mit **Pydantic v2**
- Speicherung aller Rohereignisse in **MongoDB**
- Pflege eines separaten **aktuellen Gerätezustands** pro Gerät
- Geo-Abfragen über **2dsphere**
- Filterung nach niedrigem Batteriestand
- asynchroner Datenbankzugriff mit **Motor**
- automatische API-Dokumentation über **FastAPI / OpenAPI**
- containerisierte Entwicklungsumgebung mit **Docker Compose**
- Integrationstests mit **pytest**

---
## Warum dieses Projekt relevant ist

Viele Portfolio-Projekte bleiben bei einfachem CRUD stehen. Dieses Projekt geht bewusst einen Schritt weiter und bildet ein typisches Backend-Muster aus dem IoT-Umfeld nach:

- eingehende Telemetrie wird als Ereignisstrom verarbeitet
- Rohdaten und Lesezugriffe werden getrennt modelliert
- Standortdaten werden für geografische Abfragen vorbereitet
- aktuelle Zustände können effizient abgefragt werden


---


## Architektur

### Überblick

```text
[ IoT Device / Simulator ]
           |
           | HTTP / JSON
           v
[ FastAPI Backend ]
           |
           | asynchroner MongoDB-Zugriff
           v
[ MongoDB ]
```

### Verarbeitungslogik

Bei jedem `POST /api/v1/telemetry` passiert Folgendes:

1. Die eingehende JSON-Payload wird validiert.
2. Das Telemetrie-Event wird in der Collection `telemetry` gespeichert.
3. Der aktuelle Gerätezustand wird in `devices_state` aktualisiert.
4. Für Standortabfragen wird ein Geo-Feld `location` im Format `Point [lon, lat]` gepflegt.

Dadurch sind sowohl **historische Rohdaten** als auch **schnelle State-Abfragen** möglich.

Mehr Details: siehe [`docs/architecture.md`](docs/architecture.md).

---

## Tech Stack

- **Python 3.12**
- **FastAPI**
- **Uvicorn**
- **MongoDB**
- **Motor** (async MongoDB driver)
- **Pydantic v2**
- **Docker / Docker Compose**
- **pytest**

---

## Projektstruktur

```text
app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── device_state.py
│       │   ├── health.py
│       │   └── telemetry.py
│       └── router.py
├── db/
│   └── mongo.py
├── models/
│   ├── device_state.py
│   ├── geo.py
│   └── telemetry.py
├── repositories/
│   └── telemetry_repo.py
├── services/
│   ├── device_state_service.py
│   └── telemetry_service.py
└── main.py

docs/
└── architecture.md

tests/
├── conftest.py
├── test_health.py
├── test_state_near.py
└── test_telemetry_flow.py
```

---

## API-Endpunkte

### Health

- `GET /api/v1/health` – einfacher Health-Check
- `GET /api/v1/db-ping` – prüft die Verbindung zu MongoDB
- `GET /api/v1/db-name` – zeigt den aktuell verwendeten Datenbanknamen

### Telemetry

- `POST /api/v1/telemetry` – neues Telemetrie-Event anlegen
- `GET /api/v1/telemetry` – Telemetrie-Events auflisten
- `GET /api/v1/telemetry/{telemetry_id}` – einzelnes Event per ID abrufen

### Device State

- `GET /api/v1/state` – aktuelle Zustände aller Geräte
- `GET /api/v1/state/{device_id}` – aktuellen Zustand eines Geräts abrufen
- `GET /api/v1/state/low-battery?lt=20` – Geräte mit Batteriestand unter Schwellwert
- `GET /api/v1/state/near?lat=...&lon=...&radius_m=...` – Geräte in der Nähe eines Standorts

---

## Beispiel-Payload

```json
{
  "device_id": "truck-42",
  "lat": 48.137154,
  "lon": 11.576124,
  "battery": 87,
  "timestamp": "2026-01-21T10:15:30Z"
}
```

---

## Beispiel-Response

```json
{
  "id": "65b3f1f62c0f1d0f0f123456",
  "device_id": "truck-42",
  "lat": 48.137154,
  "lon": 11.576124,
  "battery": 87,
  "timestamp": "2026-01-21T10:15:30Z",
  "ingested_at": "2026-01-21T10:15:31.224000Z"
}
```

---

## Lokale Entwicklung mit Docker Compose

### 1. Repository klonen

```bash
git clone <REPOSITORY_URL>
cd iot-fleet-backend
```

### 2. `.env` anlegen

Beispiel:

```env
MONGODB_URI=mongodb://mongo:27017
MONGODB_DB=iot_fleet
```

### 3. Container starten

```bash
docker compose up --build
```

Die Anwendung ist danach erreichbar unter:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Lokale Entwicklung ohne Docker

### 1. Virtuelle Umgebung erstellen

```bash
python -m venv .venv
source .venv/bin/activate
```

Unter Windows:

```powershell
.venv\Scripts\activate
```

### 2. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 3. Umgebungsvariablen setzen

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=iot_fleet
```

### 4. Anwendung starten

```bash
uvicorn app.main:app --reload
```

---

## Beispielaufrufe mit `curl`

### Health-Check

```bash
curl http://localhost:8000/api/v1/health
```

### Telemetrie senden

```bash
curl -X POST http://localhost:8000/api/v1/telemetry \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "scooter-9",
    "lat": 48.137154,
    "lon": 11.576124,
    "battery": 80,
    "timestamp": "2026-01-26T08:00:00Z"
  }'
```

### Aktuellen Gerätezustand abrufen

```bash
curl http://localhost:8000/api/v1/state/scooter-9
```

### Geräte in der Nähe suchen

```bash
curl "http://localhost:8000/api/v1/state/near?lat=48.137154&lon=11.576124&radius_m=1000"
```

---

## Tests

Die Tests verwenden MongoDB. Für Geo-Abfragen (`$near`, `2dsphere`) wird eine echte MongoDB-Instanz benötigt.

### Tests ausführen

```bash
pytest
```

### Geo-Integrationstests aktivieren

```bash
RUN_MONGO_INTEGRATION=1 pytest
```

Hinweis: In Docker Compose verwendet das Projekt standardmäßig den Hostnamen `mongo`.

---

## Datenmodell

### Collection `telemetry`
Speichert alle eingehenden Rohereignisse.

Beispiel-Felder:
- `_id`
- `device_id`
- `lat`
- `lon`
- `battery`
- `timestamp`
- `ingested_at`

### Collection `devices_state`
Speichert pro Gerät genau einen aktuellen Zustand.

Beispiel-Felder:
- `_id` = `device_id`
- `device_id`
- `lat`
- `lon`
- `location` (`Point`, `[lon, lat]`)
- `battery`
- `timestamp`
- `ingested_at`
- `last_event_id`

---

## Besondere technische Punkte

- **Asynchroner Zugriff** auf MongoDB über Motor
- **2dsphere-Index** auf `devices_state.location`
- **Separates State-Read-Modell** für schnelle Abfragen
- Gute Grundlage für Erweiterungen wie:
  - JWT Authentication
  - Background Jobs
  - Rate Limiting
  - Monitoring
  - Message Queue / Event Streaming

---

## Mögliche Erweiterungen

- Authentifizierung und Rollenmodell
- Gerätestammdaten (`devices` Collection)
- Pagination mit Metadaten / Cursor-basiert
- MQTT- oder Kafka-Anbindung
- Alerts bei Low Battery oder Offline-Geräten
- Prometheus-Metriken und strukturiertes Logging
- CI/CD Pipeline mit Linting, Tests und Deployment



