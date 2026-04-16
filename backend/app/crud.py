from sqlalchemy.orm import Session

from . import models, schemas


def create_saved_trip(db: Session, trip: schemas.SavedTripCreate) -> models.SavedTrip:
    db_trip = models.SavedTrip(
        destination=trip.destination,
        start_date=trip.start_date,
        end_date=trip.end_date,
        budget=trip.budget,
        interests=trip.interests,
        itinerary=[day.dict() for day in trip.itinerary],
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


def get_saved_trips(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.SavedTrip).offset(skip).limit(limit).all()
