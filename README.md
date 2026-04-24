# ViajaSencillo

Aplicación inicial de Travel Planner Inteligente con frontend Angular y backend Python + FastAPI.

## Características

- **Planificación de viajes**: Genera itinerarios personalizados basados en destino, presupuesto y preferencias
- **Previsión del clima**: Integración con Open-Meteo API para mostrar pronóstico meteorológico del destino
- **Atracciones reales**: Utiliza Open Trip Map para mostrar puntos de interés reales con ubicación exacta
- **Asistente IA**: Chat con inteligencia artificial (Mistral-7B) para responder preguntas sobre viajes
- **Autenticación completa**: Registro, login, logout y edición de perfil de usuario
- **Gestión de viajes**: Guardar y consultar viajes planificados
- **Base de datos**: Almacenamiento persistente con SQLite
- **Historial de chat**: Guarda todas las conversaciones del usuario

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

### Chat IA
- `POST /api/chat` envía un mensaje al asistente IA y obtiene respuesta (requiere token Bearer).
- `GET /api/chat/history` obtiene el historial de chat del usuario (requiere token Bearer).

## APIs Externas

### Open-Meteo (Clima)
La aplicación utiliza la **API Open-Meteo** para obtener información meteorológica de los destinos:
- **URL**: https://api.open-meteo.com
- **Características**: Geocodificación y pronóstico del clima de hasta 16 días
- **Ventajas**: Gratis, sin API key requerida, datos precisos
- **Integración**: Automática en el endpoint `POST /api/planner`

### Open Trip Map (Atracciones y Puntos de Interés)
La aplicación utiliza la **API Open Trip Map** para generar itinerarios con atracciones reales:
- **URL**: https://api.opentripmap.com
- **Características**: Más de 3 millones de puntos de interés (museos, restaurantes, naturaleza, etc.)
- **Ventajas**: Gratis, sin API key requerida, datos reales filtrados por intereses
- **Integración**: Automática en el endpoint `POST /api/planner`
- **Fallback**: Si la API no está disponible, usa datos locales

### Hugging Face (Chat IA)
La aplicación utiliza la **API Hugging Face** para proporcionar un asistente de viajes con IA:
- **URL**: https://api-inference.huggingface.co
- **Modelo**: Mistral-7B-Instruct (modelo gratuito y potente)
- **Características**: Responde preguntas sobre viajes, destinos, presupuestos, actividades
- **Configuración**: Requiere configurar la variable de entorno `HF_TOKEN`
  
#### Obtener tu HF_TOKEN:
1. Ve a https://huggingface.co/settings/tokens
2. Crea un nuevo token (acceso de lectura es suficiente)
3. Configura la variable de entorno antes de iniciar el backend:
   ```bash
   export HF_TOKEN="tu_token_aqui"
   python3 -m uvicorn app.main:app --reload
   ```
   O en Windows:
   ```cmd
   set HF_TOKEN=tu_token_aqui
   python3 -m uvicorn app.main:app --reload
   ```

## Base de datos

La aplicación usa SQLite. La base de datos se crea automáticamente al iniciar el backend.
