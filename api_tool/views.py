from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.main import get_db
from . import actions, schemas

router = APIRouter()


@router.get(
    '/{shortened_url}',
    description='取得原始網址'
)
def get_original_url(
        shortened_url: str,
        db: Session = Depends(get_db)
):
    result = actions.get_original_url(
        shortened_url=shortened_url,
        db=db
    )
    return result


@router.post(
    '/shortened_url',
    description='取得縮短網址',
    response_model=str
)
def get_shortened_url(
        inputs: schemas.UrlIn = Body(..., description='原始網址'),
        db: Session = Depends(get_db)
):
    result = actions.get_shortened_url(
        url=inputs.url,
        db=db
    )
    return result
