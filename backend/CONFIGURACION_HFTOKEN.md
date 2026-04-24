# 🔑 CONFIGURACIÓN DE HF_TOKEN

## ¿Qué se ha hecho?

✅ Archivo `.env` creado en `/workspaces/ViajaSencillo/backend/.env`
✅ `python-dotenv` instalado en `requirements.txt`
✅ Backend actualizado para cargar automáticamente variables de entorno
✅ `.gitignore` configurado para no subir el `.env` a git

## 📝 PRÓXIMO PASO: Configurar tu HF_TOKEN

### 1. Obtener Token de Hugging Face

1. Ve a: https://huggingface.co/settings/tokens
2. Haz clic en **"New token"**
3. Completa:
   - **Name**: `ViajaSencillo`
   - **Access type**: `Read`
4. Copia el token completo (empieza con `hf_`)

### 2. Editar el archivo `.env`

Abre el archivo: `/workspaces/ViajaSencillo/backend/.env`

```env
# Reemplaza esto:
HF_TOKEN=hf_tu_token_aqui

# Con tu token real:
HF_TOKEN=hf_AbCdEfGhIjKlMnOpQrStUvWxYz123456
```

Ejemplo real (NO uses este, es falso):
```env
HF_TOKEN=hf_wqKvLmNoPqRstuVwXyZaBcDeFgHiJkLm
```

### 3. Guardar y Listo

Una vez guardado el `.env` con tu token real, el chat IA funcionará automáticamente.

## 🚀 Cómo Iniciar el Backend

```bash
cd /workspaces/ViajaSencillo/backend
python3 -m uvicorn app.main:app --reload
```

El backend cargará automáticamente el token desde el archivo `.env`.

## 📦 Dependencias Instaladas

✅ fastapi==0.104.0
✅ uvicorn[standard]==0.23.2
✅ pydantic==2.8.0
✅ SQLAlchemy==2.0.23
✅ httpx==0.25.2
✅ python-dotenv==1.0.0 (NUEVO)
✅ email-validator==2.3.0

## ⚠️ Notas de Seguridad

- **NO** compartas tu `.env` con nadie
- **NO** hagas commit del `.env` a git (ya tiene .gitignore)
- **NO** pongas el token en el código
- El `.env` solo debe estar en tu máquina local

¿Necesitas ayuda para obtener el token? Pregunta en el chat. 💬
