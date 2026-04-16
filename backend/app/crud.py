import hashlib
from sqlalchemy.orm import Session

from . import models, schemas


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_saved_trip(db: Session, user_id: int, trip: schemas.SavedTripCreate) -> models.SavedTrip:
    db_trip = models.SavedTrip(
        user_id=user_id,
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


def get_saved_trips(db: Session, user_id: int, skip: int = 0, limit: int = 20):
    return (
        db.query(models.SavedTrip)
        .filter(models.SavedTrip.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
