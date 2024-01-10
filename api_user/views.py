from app import auth
from app.main import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, actions, schemas

router = APIRouter()


@router.get(
    "/info",
    description="取得使用者資訊"
)
def get_user_list(
        user=Depends(auth.get_current_user)
):
    print(f"Authorized:{user}")
    return user


@router.post(
    "/signup",
    description="註冊新使用者"
)
def create_user(
        inputs: schemas.UserBaseIn,
        db: Session = Depends(get_db)
):
    """
    create user
    """
    try:
        result, user = actions.create_user(
            inputs=inputs,
            db=db
        )

        return {
            "success": result,
            "data": schemas.UserBaseOut(
                id=user.id,
                username=user.username,
                email=user.email
            )
        }
    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }


@router.get(
    "/{user_id}",
    response_model=schemas.UserBaseOut,
    description="取得使用者資訊"
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return schemas.UserBaseOut(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email
    )
