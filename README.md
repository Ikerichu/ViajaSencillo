# ViajaSencillo

Aplicación inicial de Travel Planner Inteligente con frontend Angular y backend Python + FastAPI.

## Características

- **Planificación de viajes**: Genera itinerarios personalizados basados en destino, presupuesto y preferencias
- **Autenticación completa**: Registro, login, logout y edición de perfil de usuario
- **Gestión de viajes**: Guardar y consultar viajes planificados
- **Base de datos**: Almacenamiento persistente con SQLite

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
- `PUT /api/users/me` actualiza el perfil del usuario actual (requiere token Bearer).
- `POST /api/users/me/trips` guarda un viaje para el usuario actual (requiere token Bearer).
- `GET /api/users/me/trips` lista viajes del usuario actual (requiere token Bearer).

## Base de datos

La aplicación usa SQLite. La base de datos se crea automáticamente al iniciar el backend.
