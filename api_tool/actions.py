from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import crud


def get_original_url(
        shortened_url: str,
        db: Session
) -> str:
    original_url = crud.get_original_url(
        shortened_url=shortened_url,
        db=db
    )
    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="網址不存在"
        )
    return original_url.link


def get_shortened_url(
        url: str,
        db: Session
) -> str:
    shortened_url = crud.get_shortened_url_by_link(
        link=url,
        db=db
    )
    if shortened_url:
        return shortened_url.key
    shortened_url = crud.create_shortened_url(
        url=url,
        db=db
    )
    return shortened_url
