from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .schemas import PlannerRequest, PlannerResponse, SavedTripCreate, SavedTripResponse
from .dataset import DESTINATIONS, get_places
from .itinerary import make_itinerary
from .crud import create_saved_trip, get_saved_trips
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

@app.post("/api/trips", response_model=SavedTripResponse)
def save_trip(trip: SavedTripCreate, db: Session = Depends(get_db)):
    return create_saved_trip(db, trip)

@app.get("/api/trips", response_model=List[SavedTripResponse])
def read_saved_trips(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return get_saved_trips(db, skip=skip, limit=limit)
