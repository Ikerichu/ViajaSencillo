from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .schemas import (
    PlannerRequest,
    PlannerResponse,
    SavedTripCreate,
    SavedTripResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
    LoginResponse,
)
from .dataset import DESTINATIONS, get_places
from .itinerary import make_itinerary
from .crud import (
    authenticate_user,
    create_saved_trip,
    get_saved_trips,
    create_user,
    get_user,
    get_user_by_email,
    logout_user,
    update_user,
)
from .auth import get_current_user
from .database import engine, get_db
from .models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ViajaSencillo API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "ViajaSencillo"}

@app.get("/api/destinations")
def list_destinations() -> List[str]:
    return DESTINATIONS

@app.get("/api/places")
def place_recommendations(destination: str, interests: str = ""):
    interests_list = [interest.strip() for interest in interests.split(",") if interest.strip()]
    places = get_places(destination, interests_list)
    if not places:
        raise HTTPException(status_code=404, detail="Destino no encontrado o sin lugares registrados")
    return places

@app.post("/api/planner", response_model=PlannerResponse)
def generate_planner(request: PlannerRequest):
    itinerary = make_itinerary(request)
    days = len(itinerary)
    daily_budget = round(request.budget / days, 2) if days else 0.0
    total_cost = sum(day.estimated_cost for day in itinerary)
    notes = []
    if total_cost > request.budget:
        notes.append("Advertencia: el itinerario estimado supera tu presupuesto.")
    notes.append("Se han agrupado actividades por cercanía y preferencias.")
    return PlannerResponse(
        destination=request.destination,
        days=days,
        budget=request.budget,
        daily_budget=daily_budget,
        itinerary=itinerary,
        notes=notes,
    )

@app.post("/api/users", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    return create_user(db, user)

@app.post("/api/login", response_model=LoginResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    authenticated = authenticate_user(db, user.email, user.password)
    if not authenticated:
        raise HTTPException(status_code=401, detail="Email o contraseña incorrectos")
    return {
        "access_token": authenticated.session_token,
        "token_type": "bearer",
        "user": authenticated,
    }

@app.post("/api/logout")
def logout(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    logout_user(db, current_user.id)
    return {"message": "Sesión cerrada exitosamente"}

@app.get("/api/users/me", response_model=UserResponse)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user

@app.put("/api/users/me", response_model=UserResponse)
def update_current_user(user_update: UserUpdate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=400, detail="Email ya está en uso por otro usuario")
    return updated_user

@app.post("/api/users/me/trips", response_model=SavedTripResponse)
def save_trip(trip: SavedTripCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    return create_saved_trip(db, current_user.id, trip)

@app.get("/api/users/me/trips", response_model=List[SavedTripResponse])
def read_saved_trips(
    skip: int = 0,
    limit: int = 20,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_saved_trips(db, user_id=current_user.id, skip=skip, limit=limit)
