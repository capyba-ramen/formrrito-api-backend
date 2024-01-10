from app import models
from sqlalchemy.orm import Session, joinedload


def get_user(db: Session, user_id: int):
    return db.query(models.User).options(joinedload(models.User.todos)).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(
        username: str,
        email: str,
        hashed_password: str,
        db: Session
):
    user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(user)
    return True, user
