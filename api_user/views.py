from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.main import get_db
from . import crud

router = APIRouter()


@router.get(
    "/list",
    description="get user list"
)
def get_users():
    return "HELLO USERS"


@router.post("/")
def create_user(inputs: schemas.UserBaseIn, db: Session = Depends(get_db)):
    """
    create user
    """
    try:
        new_user = models.User(**vars(inputs), created_at=datetime.now())
        db.add(new_user)

    except Exception as ex:
        print("create user occurs error, rolling back")
        print(ex)
        db.rollback()
        raise HTTPException(status_code=500)

    db.commit()
    return {
        "Status": "Success",
        "User": schemas.UserBaseOut(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email
        )
    }


@router.get("/{user_id}", response_model=schemas.UserBaseOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return schemas.UserBaseOut(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email
    )
