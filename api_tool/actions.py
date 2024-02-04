from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from components.email import send_email, render_template
from . import crud
from .schemas import EmailIn


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


def dev_send_email(
        inputs: EmailIn
) -> bool:
    data = {
        'form': "HI capybaramen~~~~~",
        'form_link': 'http://localhost:3333/form/897eafbf-0430-47ef-83f9-f9198779674e#responses'
    }
    html = render_template('default.j2', data=data)
    send_email(
        subject=inputs.subject,
        to=inputs.to,
        body=html
    )

    return True
