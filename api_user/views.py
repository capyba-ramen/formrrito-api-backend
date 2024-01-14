from datetime import timedelta

from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session

from app import auth
from app.main import get_db
from environmemt import ACCESS_TOKEN_EXPIRE_MINUTES
from . import actions, schemas

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


@router.post(
    "/signin",
    response_model=auth.Token
)
def login_for_access_token(
        inputs: schemas.SignIn = Body(..., title="表單修改資料"),
        db: Session = Depends(get_db)
):
    """
    The response should be a JSON object
    The response should have a token_type: "bearer"
    """

    user = auth.authenticate_user(db, inputs.email, inputs.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
