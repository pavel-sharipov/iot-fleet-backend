# Architekturübersicht  
## IoT Fleet Telemetry Backend

---

## 1. Ziel der Architektur

Ziel dieser Architektur ist es, einen **skalierbaren, gut strukturierten Backend-Service** bereitzustellen, der Telemetriedaten von IoT-Geräten (z. B. Fahrzeuge, E-Scooter, Delivery-Fahrzeuge) entgegennimmt, validiert, speichert und für Analysezwecke verfügbar macht.

Der Fokus liegt auf:
- klarer Trennung von Verantwortlichkeiten (Separation of Concerns)
- Wartbarkeit und Erweiterbarkeit
- asynchroner Verarbeitung von vielen gleichzeitigen Anfragen
- Portfolio- und Praxisrelevanz

---

## 2. Gesamtarchitektur (High Level)

```
[ IoT Simulator ]
|
| HTTP (JSON)
v
[ FastAPI Backend ]
|
| async DB-Zugriff
v
[ MongoDB Atlas ]
```

---

## 3. Technologieentscheidung

### Backend
- **Python 3**
- **FastAPI** (ASGI-Framework)

**Begründung:**
- native Unterstützung von Asynchronität (`async / await`)
- automatische API-Dokumentation (Swagger / OpenAPI)
- starke Typisierung mit Pydantic
- sehr gut geeignet für API- und Microservice-Architekturen

### Datenbank
- **MongoDB Atlas (NoSQL)**

**Begründung:**
- flexible Dokumentstruktur (ideal für IoT-Daten)
- gute Unterstützung für Geo-Daten (2dsphere)
- einfache Skalierung
- Cloud-basiert (keine lokale DB-Wartung notwendig)

---

## 4. Projektstruktur
```
app/
├─ main.py # Einstiegspunkt der Anwendung
├─ api/ # API-Schicht (Router, Endpoints)
│ └─ v1/
│ ├─ router.py
│ └─ endpoints/
│ ├─ health.py
│ └─ telemetry.py
├─ schemas/ # Pydantic-Modelle (Request / Response)
├─ services/ # Business-Logik
├─ db/ # Datenbankzugriff
│ ├─ mongo.py
│ └─ repositories/
├─ core/ # Konfiguration, Logging
└─ init.py
```
---

## 5. Schichtenmodell (Layered Architecture)

### 5.1 API-Layer
- definiert HTTP-Endpunkte
- nimmt Requests entgegen
- gibt Responses zurück
- enthält **keine Business-Logik**

Beispiel:
- `POST /telemetry`
- `GET /health`

---

### 5.2 Schema-Layer
- definiert Datenstrukturen mit **Pydantic**
- validiert eingehende JSON-Daten
- stellt klare Datenverträge sicher

Beispiel:
- `TelemetryIn`
- `TelemetryOut`

---

### 5.3 Service-Layer
- enthält die fachliche Logik
- verarbeitet validierte Daten
- entscheidet über weitere Schritte (Speichern, Berechnung, Filterung)

Beispiele:
- Plausibilitätsprüfungen (Batterie 0–100 %)
- Aggregationen
- Vorbereitung für Datenbankzugriffe

---

### 5.4 Repository-Layer (Data Access Layer)
- kapselt den Zugriff auf MongoDB
- enthält CRUD-Operationen
- keine Business-Logik

Beispiele:
- `insert_telemetry()`
- `find_vehicles_by_battery()`
- Geo-Abfragen

---

## 6. Request-Ablauf (Request Flow)

Beispiel: `POST /telemetry`

1. IoT-Gerät sendet JSON-Payload
2. FastAPI empfängt die Anfrage
3. Pydantic validiert die Daten
4. Endpoint ruft Service-Layer auf
5. Service-Layer ruft Repository-Layer auf
6. Daten werden in MongoDB gespeichert
7. Antwort wird an den Client zurückgegeben

---

## 7. Asynchrones Modell

Das Backend verwendet ein **asynchrones Verarbeitungsmodell**:

- gleichzeitige Verarbeitung vieler Anfragen
- keine Blockierung während Datenbankzugriffen
- geeignet für hohe Request-Frequenzen (IoT-Szenarien)

ASGI-Server:
- **Uvicorn**

---

## 8. Versionierung der API

Die API ist versioniert:
/api/v1/...

Vorteile:
- spätere Erweiterungen ohne Breaking Changes
- paralleler Betrieb mehrerer Versionen möglich

---

## 9. Erweiterbarkeit

Die Architektur erlaubt einfache Erweiterungen, z. B.:
- Authentifizierung (JWT)
- Rollen (Admin / Operator)
- Hintergrundjobs
- Monitoring & Logging
- CI/CD-Integration

---

## 10. Fazit

Diese Architektur:
- folgt modernen Backend-Best Practices
- ist leicht verständlich und wartbar
- eignet sich ideal für Lern-, Demo- und Portfolio-Zwecke
- bildet reale IoT-Backend-Szenarien realistisch ab
