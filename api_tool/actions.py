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
    return original_url


def get_shortened_url(
        url: str,
        db: Session
) -> str:
    shortened_url = crud.get_shortened_url_by_link(
        link=url,
        db=db
    )
    if shortened_url:
        return shortened_url
    shortened_url = crud.create_shortened_url(
        url=url,
        db=db
    )
    return shortened_url
