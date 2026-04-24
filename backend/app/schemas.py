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

class WeatherDay(BaseModel):
    date: str
    temp_max: float
    temp_min: float
    precipitation: float
    weather_code: int

class WeatherInfo(BaseModel):
    location_name: str
    country: str
    timezone: str
    forecast: List[WeatherDay]

class PlannerResponse(BaseModel):
    destination: str
    days: int
    budget: float
    daily_budget: float
    itinerary: List[ItineraryDay]
    notes: List[str]
    weather: WeatherInfo = None

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

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
        from_attributes = True


class ChatMessageCreate(BaseModel):
    content: str


class ChatMessageResponse(BaseModel):
    id: int
    user_id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
