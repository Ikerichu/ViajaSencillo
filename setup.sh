#!/bin/bash

# 🚀 ViajaSencillo - Quick Setup Script
# Ejecutar este script para configurar el proyecto automáticamente

set -e

echo "================================"
echo "ViajaSencillo - Setup Automático"
echo "================================"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para imprimir en color
print_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
  echo -e "${RED}❌ $1${NC}"
}

# Verificar requisitos
echo -e "${YELLOW}Verificando requisitos...${NC}"

if ! command -v python3 &> /dev/null; then
  print_error "Python 3 no encontrado. Por favor instala Python 3.12+"
  exit 1
fi

if ! command -v node &> /dev/null; then
  print_error "Node.js no encontrado. Por favor instala Node.js 18+"
  exit 1
fi

if ! command -v npm &> /dev/null; then
  print_error "npm no encontrado. Por favor instala npm"
  exit 1
fi

print_success "Python3 instalado: $(python3 --version)"
print_success "Node.js instalado: $(node --version)"
print_success "npm instalado: $(npm --version)"

echo ""
echo -e "${YELLOW}Configurando Backend...${NC}"

# Backend setup
cd backend

# Crear virtualenv
if [ ! -d "venv" ]; then
  print_warning "Creando virtualenv..."
  python3 -m venv venv
fi

# Activar virtualenv
source venv/bin/activate

# Instalar dependencias
print_warning "Instalando dependencias Python..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt > /dev/null

# Crear DB
print_warning "Inicializando base de datos..."
python3 -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)" 2>/dev/null || true

print_success "Backend configurado"

cd ..

echo ""
echo -e "${YELLOW}Configurando Frontend...${NC}"

# Frontend setup
cd frontend

# Instalar dependencias
print_warning "Instalando dependencias Node..."
npm install > /dev/null

print_success "Frontend configurado"

cd ..

echo ""
echo "================================"
print_success "¡Configuración completada!"
echo "================================"

echo ""
echo -e "${GREEN}Próximos pasos:${NC}"
echo ""
echo "1️⃣  Configurar Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python3 -m uvicorn app.main:app --reload --port 8000"
echo ""
echo "   Backend estará en http://localhost:8000"
echo "   Docs en http://localhost:8000/docs"
echo ""
echo "2️⃣  Configurar Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "   Frontend estará en http://localhost:4200"
echo ""
echo -e "${YELLOW}Opcional:${NC}"
echo "   Para usar chat con IA, configura .env en backend/"
echo "   Agregar: HF_TOKEN=tu_token_de_huggingface"
echo ""
echo "3️⃣  Ejecutar tests:"
echo "   cd backend"
echo "   python3 test_e2e.py"
echo ""
echo "================================"
