import hashlib
import uuid
from sqlalchemy.orm import Session

from . import models, schemas


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


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


def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.session_token == token).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    user.session_token = uuid.uuid4().hex
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def logout_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        user.session_token = None
        db.add(user)
        db.commit()
        return True
    return False


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None
    # Check if email is already taken by another user
    existing_user = get_user_by_email(db, user_update.email)
    if existing_user and existing_user.id != user_id:
        return None
    user.name = user_update.name
    user.email = user_update.email
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


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


def create_chat_message(db: Session, user_id: int, role: str, content: str):
    db_message = models.ChatMessage(
        user_id=user_id,
        role=role,
        content=content,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_chat_history(db: Session, user_id: int, limit: int = 50):
    return (
        db.query(models.ChatMessage)
        .filter(models.ChatMessage.user_id == user_id)
        .order_by(models.ChatMessage.created_at.asc())
        .limit(limit)
        .all()
    )
