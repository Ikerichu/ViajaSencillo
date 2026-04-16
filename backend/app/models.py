from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, JSON

from .database import Base


class SavedTrip(Base):
    __tablename__ = "saved_trips"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, index=True, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    budget = Column(Float, nullable=False)
    interests = Column(JSON, nullable=False)
    itinerary = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
