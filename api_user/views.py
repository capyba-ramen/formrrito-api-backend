from app import models, schemas, auth
from app.auth import hash_password
from app.main import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud

router = APIRouter()


@router.get(
    "/info",
    description="get user list"
)
def get_user_list(
        user=Depends(auth.get_current_user)
):
    print(f"Authorized:{user}")
    return user


@router.post(
    "/",
    description="註冊新使用者",
    operation_id="create_user",
)
def create_user(
        inputs: schemas.UserBaseIn,
        db: Session = Depends(get_db)
):
    """
    create user
    """
    try:
        new_user = models.User(
            username=inputs.username,
            email=inputs.email,
            hashed_password=hash_password(inputs.password)
        )
        db.add(new_user)
        db.commit()
    except Exception as ex:
        print("create user occurs error, rolling back")
        print(ex)
        db.rollback()
        return False

    return {
        "success": True,
        "data": schemas.UserBaseOut(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email
        )
    }


@router.get("/{user_id}", response_model=schemas.UserBaseOut, operation_id="get_user")
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return schemas.UserBaseOut(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email
    )
