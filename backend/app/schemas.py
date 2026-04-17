from datetime import date, datetime
from typing import List
from pydantic import BaseModel, EmailStr

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

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class SavedTripCreate(BaseModel):
    destination: str
    start_date: date
    end_date: date
    budget: float
    interests: List[str]
    itinerary: List[ItineraryDay]

class SavedTripResponse(BaseModel):
    id: int
    user_id: int
    destination: str
    start_date: date
    end_date: date
    budget: float
    interests: List[str]
    itinerary: List[ItineraryDay]
    created_at: datetime

    class Config:
        orm_mode = True
