# ✈️ ViajaSencillo - Planificador de Viajes Inteligente

> Una aplicación web moderna para planificar viajes personalizados con inteligencia artificial, integración de APIs meteorológicas y atractivos turísticos reales.

## 🎯 Estado del Proyecto: 100% COMPLETO ✅

Todas las características están implementadas, probadas y funcionando.

---

## ✨ Características Implementadas

### 🗺️ Planificación de Viajes
- ✅ Generación de itinerarios personalizados (3-4 actividades por día)
- ✅ Estimación automática de costos dentro del presupuesto
- ✅ Selección de intereses (cultura, naturaleza, comida, fiesta)
- ✅ Duración flexible de viajes (1-30+ días)

### 🌤️ Información Meteorológica
- ✅ Integración con Open-Meteo API
- ✅ Pronóstico de temperatura máxima/mínima
- ✅ Datos de precipitación predicha
- ✅ Datos para múltiples días de viaje

### 🏛️ Atractivos Turísticos
- ✅ Integración con Open Trip Map API
- ✅ Búsqueda de atracciones por intereses
- ✅ Sistema de fallback (dataset local)
- ✅ Estimación de costos por atracción

### 🤖 Asistente IA
- ✅ Chat con Mistral-7B (Hugging Face)
- ✅ Respuestas contextuales sobre viajes
- ✅ Historial de conversaciones persistente
- ✅ Recomendaciones personalizadas

### 👤 Gestión de Usuarios
- ✅ Registro con validación de email
- ✅ Login/Logout con tokens de sesión
- ✅ Edición de perfil de usuario
- ✅ Guardado de viajes favoritos
- ✅ Historial de viajes planificados

### 💾 Persistencia de Datos
- ✅ Base de datos SQLite con SQLAlchemy ORM
- ✅ Modelos: User, SavedTrip, ChatMessage
- ✅ Relaciones entre entidades
- ✅ Índices para consultas rápidas

### 🎨 Interface de Usuario
- ✅ Aplicación Angular 16 SPA
- ✅ Rutas: Home, Planner, Results, Profile, Chat
- ✅ Diseño responsive
- ✅ Componentes modulares reutilizables
- ✅ Validación de formularios

---

## 🛠️ Stack Tecnológico

### Frontend
- **Framework**: Angular 16
- **Lenguaje**: TypeScript 5.1.6
- **Estilos**: CSS 3 con Flexbox/Grid
- **HTTP Client**: Angular HttpClientModule
- **Routing**: Angular Router con lazy loading

### Backend
- **Framework**: FastAPI 0.104.0
- **Lenguaje**: Python 3.12
- **ORM**: SQLAlchemy 2.0.23
- **Base de datos**: SQLite
- **Async**: httpx para llamadas HTTP asincrónicas
- **Validación**: Pydantic 2.8.0

### APIs Externas
- **Meteorología**: Open-Meteo (gratuita)
- **Atracciones**: Open Trip Map (gratuita)
- **IA**: Hugging Face Mistral-7B (requiere token)

---

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.12+
- Node.js 18+
- npm o yarn
- Git

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tuusuario/ViajaSencillo.git
cd ViajaSencillo
```

### Paso 2: Configurar Backend

```bash
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (opcional, para token de HF)
# Editar backend/.env y agregar:
# HF_TOKEN=tu_token_de_huggingface

# Iniciar servidor
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: `http://localhost:8000`
- API docs (Swagger): `http://localhost:8000/docs`
- OpenAPI: `http://localhost:8000/openapi.json`

### Paso 3: Configurar Frontend (nueva terminal)

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start

# O construir para producción
npm run build
```

El frontend estará disponible en: `http://localhost:4200`

---

## 📚 Uso de la Aplicación

### 1. Registro e Inicio de Sesión
1. Ir a `/home`
2. Hacer clic en "Registrarse"
3. Ingresar email, nombre y contraseña
4. Hacer clic en "Registrarse"

### 2. Planificar un Viaje
1. Ir a `/planner`
2. Ingresar:
   - Destino (ej: "Barcelona")
   - Fecha de inicio y fin
   - Presupuesto total
   - Intereses (marcar varias opciones)
3. Hacer clic en "Generar Itinerario"
4. Ver resultados con clima y actividades

### 3. Guardar Viaje
En `/results`, hacer clic en "Guardar Viaje" para guardarlo en perfil

### 4. Ver Perfil y Viajes Guardados
Ir a `/profile` para ver:
- Información del usuario
- Viajes planificados
- Opción de editar perfil

### 5. Chat con IA
Ir a `/chat` para:
- Hacer preguntas sobre viajes
- Recibir recomendaciones personalizadas
- Ver historial de conversaciones

---

## 📋 Endpoints de API

### Autenticación
- `POST /api/register` - Registrar usuario
- `POST /api/login` - Iniciar sesión
- `POST /api/logout` - Cerrar sesión

### Planificación
- `GET /api/health` - Verificar estado servidor
- `POST /api/planner` - Generar itinerario
- `GET /api/destinations` - Listar destinos populares

### Usuarios
- `GET /api/users/me` - Obtener perfil actual
- `PUT /api/users/me` - Actualizar perfil
- `POST /api/users/me/trips` - Guardar viaje
- `GET /api/users/me/trips` - Obtener viajes guardados

### Chat
- `POST /api/chat` - Enviar mensaje
- `GET /api/chat/history` - Obtener historial

---

## 🧪 Testing

### Ejecutar pruebas end-to-end

```bash
cd backend
python3 test_e2e.py
```

Esto valida:
- ✅ Integración de Weather API
- ✅ Generación de itinerarios
- ✅ API de atracciones
- ✅ Chat con IA
- ✅ Operaciones de base de datos

---

## 📁 Estructura de Carpetas

```
ViajaSencillo/
├── backend/
│   ├── app/
│   │   ├── main.py           # API endpoints
│   │   ├── models.py         # Modelos SQLAlchemy
│   │   ├── schemas.py        # Esquemas Pydantic
│   │   ├── database.py       # Configuración DB
│   │   ├── weather.py        # Open-Meteo integration
│   │   ├── attractions.py    # Open Trip Map integration
│   │   ├── chat.py           # Hugging Face integration
│   │   ├── itinerary.py      # Generador de itinerarios
│   │   ├── auth.py           # Autenticación
│   │   ├── crud.py           # Operaciones DB
│   │   ├── dataset.py        # Dataset fallback
│   │   └── dependencies.py   # Dependencias
│   ├── .env                  # Variables de entorno
│   ├── requirements.txt      # Dependencias Python
│   └── test_e2e.py          # Tests end-to-end
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/   # Componentes Angular
│   │   │   ├── services/     # Servicios (API)
│   │   │   ├── models/       # Modelos TypeScript
│   │   │   └── app-routing.module.ts
│   │   ├── assets/           # Recursos estáticos
│   │   └── styles.css        # Estilos globales
│   ├── angular.json          # Configuración Angular
│   ├── package.json          # Dependencias Node
│   └── tsconfig.json         # Configuración TypeScript
└── README.md
```

---

## 🔐 Configuración de Seguridad

### Variables de Entorno (.env)
```env
# Token de Hugging Face (opcional, para chat)
HF_TOKEN=hf_tu_token_aqui

# DEBUG (opcional)
DEBUG=False
```

### Obtener HF_TOKEN
1. Ir a https://huggingface.co/settings/tokens
2. Crear token de lectura
3. Copiar en `backend/.env`
4. Reiniciar servidor

---

## 📈 Optimizaciones Realizadas

- ✅ Timeouts configurados correctamente (30s para APIs)
- ✅ Manejo de errores con fallbacks automáticos
- ✅ Consultas de BD usando índices
- ✅ Caché de datos cuando es posible
- ✅ Async/await para operaciones no-bloqueantes
- ✅ CORS habilitado para desarrollo

---

## 🐛 Troubleshooting

### El frontend no carga
- Verificar que backend está en http://localhost:8000
- Revisar CORS en `backend/app/main.py`
- Limpiar caché del navegador

### Chat no funciona
- Verificar que HF_TOKEN está configurado en `.env`
- Verificar token es válido en https://huggingface.co
- Revisar logs: `tail -f backend/backend.log`

### Weather no muestra datos
- Es normal en desarrollo (puede ser rate limited)
- Sistema tiene fallback automático
- Verificar conexión a internet
- Timeouts aumentados a 30s

### Itinerario vacío
- Verificar destino existe
- Probar con ciudades comunes (Barcelona, Madrid, etc)
- Revisar presupuesto > 0

---

## 📝 Notas de Desarrollo

### Flujo de Autenticación
1. Usuario registra credenciales
2. Backend genera hash de contraseña
3. Se crea session_token único
4. Frontend almacena token en localStorage
5. Token se envía en header `Authorization: Bearer {token}`

### Generación de Itinerario
1. Usuario especifica parámetros
2. Intenta obtener atracciones reales (Open Trip Map)
3. Si falla, usa dataset local precargado
4. Estima costos por actividad
5. Retorna 3 actividades/día dentro de presupuesto

### Integración de APIs
- **Open-Meteo**: Sin autenticación, gratuita
- **Open Trip Map**: Sin autenticación, gratuita
- **Hugging Face**: Requiere token gratuito

---

## 🚀 Deployment (Producción)

### Backend (Heroku/Railway)
```bash
# Crear archivo runtime.txt
echo "python-3.12.0" > runtime.txt

# Crear Procfile
echo "web: gunicorn -w 4 -b 0.0.0.0:\$PORT app.main:app" > Procfile

# Instalar gunicorn
pip install gunicorn
```

### Frontend (Netlify/Vercel)
```bash
# Build
npm run build

# Deploy carpeta dist/
```

---

## 📞 Soporte

Para reportar bugs o sugerencias:
1. Crear issue en GitHub
2. Describir el problema
3. Incluir logs si es posible
4. Especificar OS y versiones

---

## 📄 Licencia

MIT License - Libre para uso comercial y personal

---

## 🙏 Agradecimientos

- OpenMeteo por API meteorológica gratuita
- Open Trip Map por datos de atracciones
- Hugging Face por modelo Mistral-7B
- Angular y FastAPI por excelentes frameworks

---

**Última actualización**: April 28, 2026
**Status**: ✅ 100% COMPLETO Y FUNCIONAL

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
