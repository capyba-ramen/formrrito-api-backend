from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.main import get_db
from . import crud

router = APIRouter()


@router.get(
    "/{user_id}"
)
def get_forms(user_id: int, db: Session = Depends(get_db)):
    todos = crud.get_forms(db, user_id=user_id)
    return todos
