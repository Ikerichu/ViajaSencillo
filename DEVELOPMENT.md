# 🛠️ Guía de Desarrollo - ViajaSencillo

Esta guía proporciona instrucciones detalladas para desarrolladores.

## Requisitos de Desarrollo

- Python 3.12+
- Node.js 18+ (LTS recomendado)
- npm 9+
- Git
- Navegador moderno (Chrome, Firefox, Safari)

## Setup Inicial

### 1. Clonar y Estructura Base

```bash
git clone https://github.com/tuusuario/ViajaSencillo.git
cd ViajaSencillo
```

### 2. Backend Setup

```bash
cd backend

# Crear virtualenv
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env  # Si existe
# Editar .env con tus valores:
# HF_TOKEN=tu_token
# DEBUG=True

# Inicializar base de datos
python3 -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Iniciar servidor
python3 -m uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

El servidor estará en: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Frontend Setup

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
ng serve --open

# O npm start (alias de ng serve)
```

El frontend estará en: http://localhost:4200

## Estructura de Directorios

### Backend
```
backend/
├── app/
│   ├── main.py              # Punto de entrada FastAPI (13+ endpoints)
│   ├── models.py            # Modelos SQLAlchemy (User, SavedTrip, ChatMessage)
│   ├── schemas.py           # Esquemas Pydantic para validación
│   ├── database.py          # Configuración SQLAlchemy y sesiones
│   ├── weather.py           # Integración Open-Meteo
│   ├── attractions.py       # Integración Open Trip Map
│   ├── chat.py              # Integración Hugging Face
│   ├── itinerary.py         # Lógica de generación de itinerarios
│   ├── auth.py              # Funciones de autenticación
│   ├── crud.py              # Operaciones de BD
│   ├── dataset.py           # Dataset fallback de atracciones
│   ├── dependencies.py      # Dependencias inyectables
│   └── __init__.py
├── .env                     # Variables de entorno (NO commitar)
├── .gitignore              # Archivos a ignorar
├── requirements.txt        # Dependencias Python
├── test_e2e.py            # Tests end-to-end
└── venv/                   # Virtualenv (ignorado)
```

### Frontend
```
frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── home/                # Página de inicio
│   │   │   ├── planner/             # Formulario de planificación
│   │   │   ├── results/             # Visualización de resultados
│   │   │   ├── profile/             # Perfil de usuario
│   │   │   ├── chat/                # Chat con IA
│   │   │   ├── navbar/              # Navegación
│   │   │   └── login/               # Auth
│   │   ├── models/
│   │   │   ├── user.ts
│   │   │   ├── trip.ts
│   │   │   └── chat-message.ts
│   │   ├── services/
│   │   │   └── api.service.ts       # Cliente HTTP
│   │   ├── app.module.ts            # Módulo raíz
│   │   ├── app-routing.module.ts    # Rutas
│   │   └── app.component.ts         # Componente raíz
│   ├── assets/                      # Recursos estáticos
│   ├── styles.css                   # Estilos globales
│   ├── main.ts                      # Bootstrap
│   ├── index.html
│   ├── favicon.ico
│   └── environments/
│       ├── environment.ts           # Dev
│       └── environment.prod.ts      # Prod
├── dist/                            # Build output (ignorado)
├── node_modules/                    # Dependencias (ignorado)
├── angular.json                     # Configuración Angular
├── tsconfig.json                    # TypeScript config
├── tsconfig.app.json               # TypeScript app config
├── package.json                     # Dependencias Node
├── package-lock.json
└── README.md
```

## Endpoints de API Principales

### Autenticación
- `POST /api/register` - Crear cuenta
- `POST /api/login` - Iniciar sesión
- `POST /api/logout` - Cerrar sesión

### Planificación
- `POST /api/planner` - Generar itinerario
- `GET /api/destinations` - Destinos populares
- `GET /api/health` - Health check

### Usuarios
- `GET /api/users/me` - Obtener perfil
- `PUT /api/users/me` - Actualizar perfil
- `GET /api/users/me/trips` - Viajes guardados
- `POST /api/users/me/trips` - Guardar viaje

### Chat
- `POST /api/chat` - Enviar mensaje
- `GET /api/chat/history` - Historial

## Client HTTP (TypeScript)

```typescript
// Uso en servicios Angular
private api = inject(HttpClient);

// Exemplo: Generar itinerario
this.api.post('/api/planner', {
  destination: 'Barcelona',
  start_date: '2026-05-01',
  end_date: '2026-05-03',
  budget: 800,
  interests: ['cultura', 'comida']
}, {
  headers: { 'Authorization': `Bearer ${token}` }
})
```

## Testing

### Tests End-to-End
```bash
cd backend
python3 test_e2e.py
```

Verifica:
- ✅ Weather API integration
- ✅ Itinerary generation
- ✅ Attractions API
- ✅ Chat integration
- ✅ Database operations

### Pruebas Manual

#### Test Weather API
```bash
curl "https://api.open-meteo.com/v1/forecast?latitude=41.38&longitude=2.15&daily=temperature_2m_max"
```

#### Test Backend
```bash
# Registrarse
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test","password":"test123"}'

# Login
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

## Flujos Importantes

### Autenticación
1. User registra con email/password
2. Backend hashea contraseña (bcrypt)
3. Se crea session_token único
4. Frontend almacena en localStorage
5. Requets posteriores incluyen token en header

### Generación de Itinerario
1. Input: destination, dates, budget, interests
2. Intenta Open Trip Map para atracciones reales
3. Si falla, usa dataset local
4. Estima 3 actividades/día
5. Output: Itinerary con costo total

### Chat con IA
1. Usuario envía mensaje (text)
2. Backend envía a Hugging Face API
3. Recibe respuesta del modelo Mistral
4. Guarda en DB para historial
5. Retorna al frontend

## Variables de Entorno

### Backend (.env)
```env
# Hugging Face Token (opcional, para chat completo)
HF_TOKEN=hf_xxx

# Debug mode
DEBUG=True

# Database (opcional, por defecto SQLite)
# DATABASE_URL=sqlite:///./test.db
```

### Frontend (environment.ts)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8000'
};
```

## Debugging

### Backend
```python
# Usar debugger
import pdb; pdb.set_trace()

# O print statements
print(f"Debug: {variable}")

# Ver logs
tail -f backend.log
```

### Frontend
```typescript
// Chrome DevTools
console.log('Debug:', value);

// Breakpoints
debugger;

// Angular DevTools extension
```

## Performance Tips

### Backend
- Usar async/await para I/O
- Cache resultados cuando sea posible
- Índices en campos frecuentes
- Connection pooling para BD

### Frontend
- Lazy loading de rutas
- OnPush change detection strategy
- Minimizar bundle size
- Usar TrackBy en *ngFor

## Deployment Checklist

- [ ] Tests pasan (npm test, pytest)
- [ ] Linter sin errores (eslint, pylint)
- [ ] Build exitoso (npm run build)
- [ ] Variables de entorno configuradas
- [ ] Base de datos migrada
- [ ] CORS configurado correctamente
- [ ] Certificados SSL listos
- [ ] Monitoring/logging configurado

## Recursos Útiles

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Angular Docs](https://angular.io/docs)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org)
- [Pydantic](https://docs.pydantic.dev)
- [HTTP Status Codes](https://httpwg.org/specs/rfc9110.html)

## Contacto y Soporte

Para ayuda, reportar bugs o sugerencias:
- GitHub Issues
- Email: tu@email.com
- Discord: [Link del server]

---

**Última actualización**: April 28, 2026
**Versión**: 1.0.0 ✅
