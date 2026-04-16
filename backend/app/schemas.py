from datetime import date, datetime
from typing import List
from pydantic import BaseModel

class PlannerRequest(BaseModel):
    destination: str
    start_date: date
    end_date: date
    budget: float
    interests: List[str]

class ItineraryDay(BaseModel):
    day: int
    activities: List[str]
    estimated_cost: float

class PlannerResponse(BaseModel):
    destination: str
    days: int
    budget: float
    daily_budget: float
    itinerary: List[ItineraryDay]
    notes: List[str]

class SavedTripCreate(BaseModel):
    destination: str
    start_date: date
    end_date: date
    budget: float
    interests: List[str]
    itinerary: List[ItineraryDay]

class SavedTripResponse(BaseModel):
    id: int
    destination: str
    start_date: date
    end_date: date
    budget: float
    interests: List[str]
    itinerary: List[ItineraryDay]
    created_at: datetime

    class Config:
        orm_mode = True
