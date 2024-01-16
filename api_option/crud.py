from typing import List

from sqlalchemy.orm import Session

from app.models import Option


def create_options(
        question_id: str,
        options: List[str],
        db: Session
):
    for option in options:
        db.add(Option(
            question_id=question_id,
            title=option
        ))
        db.flush()
    return True


def get_option_by_id(
        option_id: int,
        db: Session
):
    return db.query(Option).filter(
        Option.id == option_id
    ).first()


def update_option(
        option: Option,
        title: str
):
    option.title = title

    return True


def delete_option(
        option: Option,
        db: Session
):
    db.delete(option)
    return True
