from app.auth import hash_password
from components.db_decorators import transaction

from . import crud


@transaction
def create_user(
        inputs,
        db
):
    result, user = crud.create_user(
        username=inputs.username,
        email=inputs.email,
        hashed_password=hash_password(inputs.password),
        db=db
    )

    return result, user
