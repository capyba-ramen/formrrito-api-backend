from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.main import get_db
from . import actions, schemas

router = APIRouter()


@router.get(
    '/shortened_url/{shortened_url}',
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


@router.post(
    "/email",
    description="寄送email(測試用)",
    response_model=bool,
    # include_in_schema=False
)
def dev_send_email(
        inputs: schemas.EmailIn = Body(..., description='email內容')
):
    result = actions.dev_send_email(
        inputs=inputs
    )
    return result
