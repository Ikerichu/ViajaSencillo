#!/bin/bash

# ViajaSencillo - Start All Services Script
# Starts both backend (FastAPI) and frontend (Angular) concurrently

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║  ViajaSencillo - Starting All Services ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
    echo ""
}

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Cleanup function on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down services...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

trap cleanup SIGTERM SIGINT

print_header

# Check requirements
echo -e "${YELLOW}Checking requirements...${NC}"

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found"
    exit 1
fi
print_status "Python3 found"

if ! command -v npm &> /dev/null; then
    echo "ERROR: npm not found"
    exit 1
fi
print_status "npm found"

# Install dependencies if needed
if [ ! -d "backend/venv" ] && [ ! -d "backend/.venv" ]; then
    print_warning "Backend virtualenv not found, installing..."
    python3 -m venv backend/venv
    source backend/venv/bin/activate
    pip install -r backend/requirements.txt > /dev/null
    deactivate
fi

if [ ! -d "node_modules" ]; then
    print_warning "Frontend dependencies not found, installing..."
    npm install > /dev/null
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}Starting Services...${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""

# Start Backend
echo -e "${BLUE}Starting Backend (FastAPI)...${NC}"
cd "$PROJECT_ROOT/backend"
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 3000 > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
print_status "Backend started (PID: $BACKEND_PID)"
print_status "Backend available at: http://localhost:3000"
print_status "Swagger UI: http://localhost:3000/docs"
echo ""

# Start Frontend
echo -e "${BLUE}Starting Frontend (Angular)...${NC}"
cd "$PROJECT_ROOT/frontend"
npm start > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
print_status "Frontend started (PID: $FRONTEND_PID)"
print_status "Frontend available at: http://localhost:4200"
echo ""

# Wait for services to be ready
echo -e "${YELLOW}Waiting for services to start...${NC}"
sleep 3

# Check if services are running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo -e "${YELLOW}Backend startup failed. Checking logs:${NC}"
    cat /tmp/backend.log
    exit 1
fi

if ! ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${YELLOW}Frontend startup failed. Checking logs:${NC}"
    cat /tmp/frontend.log
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     ✨ All Services Started! ✨       ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Backend:${NC}  http://localhost:3000"
echo -e "${BLUE}Frontend: http://localhost:4200"
echo -e "${BLUE}API Docs: http://localhost:3000/docs"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Monitor processes
while true; do
    if ! ps -p $BACKEND_PID > /dev/null; then
        echo -e "${YELLOW}Backend process died. Exiting...${NC}"
        kill $FRONTEND_PID 2>/dev/null || true
        exit 1
    fi
    if ! ps -p $FRONTEND_PID > /dev/null; then
        echo -e "${YELLOW}Frontend process died. Exiting...${NC}"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done
