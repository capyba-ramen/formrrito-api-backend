from typing import List

from sqlalchemy.orm import Session

from app.models import Option
from . import schemas


def create_options(
        question_id: str,
        titles: List[str],
        db: Session
):
    for title in titles:
        db.add(Option(
            question_id=question_id,
            title=title
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


def get_options_by_question_id(
        question_id: str,
        db: Session
):
    return db.query(Option).filter(
        Option.question_id == question_id
    ).all()


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
