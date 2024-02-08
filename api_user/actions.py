from fastapi import HTTPException, status

from app.auth import hash_password
from components.db_decorators import transaction
from . import crud


@transaction
def create_user(
        inputs,
        db
):
    user = crud.get_user_by_email(db, inputs.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    result, user = crud.create_user(
        username=inputs.username,
        email=inputs.email,
        hashed_password=hash_password(inputs.password),
        db=db
    )

    return result, user
