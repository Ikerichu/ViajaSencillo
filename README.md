# ViajaSencillo

Aplicación inicial de Travel Planner Inteligente con frontend Angular y backend Python + FastAPI.

## Estructura

- `frontend/`: aplicación Angular SPA con rutas `/home`, `/planner`, `/results`, `/profile`
- `backend/`: API REST en FastAPI para generar itinerarios y recomendaciones

## Iniciar backend

```bash
cd backend
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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

### Autenticación

- `POST /api/users` registra un nuevo usuario con `name`, `email`, `password`.
- `POST /api/login` inicia sesión con `email`, `password` y devuelve token Bearer.
- `POST /api/logout` cierra sesión (requiere token Bearer).
- `GET /api/users/me` obtiene datos del usuario actual (requiere token Bearer).
- `POST /api/users/me/trips` guarda un viaje para el usuario actual (requiere token Bearer).
- `GET /api/users/me/trips` lista viajes del usuario actual (requiere token Bearer).

## Base de datos

La aplicación usa SQLite. La base de datos se crea automáticamente al iniciar el backend.
