import uuid

from sqlalchemy.orm import Session

from app.models import Question
from . import schemas


def get_question_by_id(question_id: str, db: Session):
    form = db.query(Question).filter(Question.id == question_id).first()
    return form


def create_question(
        form_id: str,
        db: Session
):
    question_id = str(uuid.uuid4())
    question = Question(
        id=question_id,
        form_id=form_id,
        order=0
    )
    db.add(question)
    return question_id


def update_question(
        question: Question,
        fields: schemas.UpdateQuestionIn
):
    if fields.title:
        question.title = fields.title
    if fields.description:
        question.description = fields.description
    if fields.type:
        question.type = fields.type
    if fields.is_required is not None:
        question.is_required = fields.is_required

    return True


def delete_question(
        question: Question,
        db: Session
):
    db.delete(question)
    return True
