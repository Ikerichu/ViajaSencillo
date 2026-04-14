# ViajaSencillo

Aplicación inicial de Travel Planner Inteligente con frontend Angular y backend Python + FastAPI.

## Estructura

- `frontend/`: aplicación Angular SPA con rutas `/home`, `/planner`, `/results`, `/profile`
- `backend/`: API REST en FastAPI para generar itinerarios y recomendaciones

## Iniciar backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Iniciar frontend

```bash
cd frontend
npm install
npm start
```

## Iniciar desde la raíz

```bash
npm install
npm run start
```

## API principal

- `GET /api/health` verifica el backend.
- `GET /api/destinations` lista destinos disponibles.
- `GET /api/places?destination=<ciudad>&interests=<lista>` devuelve recomendaciones de lugares.
- `POST /api/planner` genera itinerario con `destination`, `start_date`, `end_date`, `budget`, `interests`.
