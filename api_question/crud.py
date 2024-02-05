import uuid
from typing import List

from sqlalchemy.orm import Session, joinedload

from app.models import Question
from . import schemas


def get_question_by_id(question_id: str, form_id: str, db: Session):
    question_query = db.query(Question).filter(Question.id == question_id)
    if form_id:
        question_query = question_query.filter(Question.form_id == form_id)

    return question_query.first()


def get_questions_by_form_id(form_id: str, db: Session):
    return db.query(Question).filter(Question.form_id == form_id).order_by(
        Question.created_at.asc(), Question.order.asc()
    ).all()


def get_questions_with_options_by_form_id(form_id: str, db: Session):
    return db.query(Question).options(
        joinedload(Question.options)
    ).filter(Question.form_id == form_id).order_by(
        Question.created_at.asc(), Question.order.asc()
    ).all()


def create_question(
        form_id: str,
        db: Session,
        title: str = None,
        description: str = None,
        question_type: str = None,
        is_required: bool = None,
        order: int = None
):
    question_id = str(uuid.uuid4())
    question = Question(
        id=question_id,
        form_id=form_id
    )
    if title:
        question.title = title
    if description:
        question.description = description
    if question_type:
        question.type = question_type
    if is_required:
        question.is_required = is_required
    if order:
        question.order = order
    else:
        question.order = 0
    db.add(question)
    return question_id, question


def update_question(
        question: Question,
        fields: schemas.UpdateQuestionIn
):
    if fields.title:
        question.title = fields.title
    if fields.description:
        question.description = fields.description
    if fields.type is not None:
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


def change_order(
        questions: [Question],
        question_order: List[str]
):
    for index, question_id in enumerate(question_order):
        question = next(filter(lambda q: q.id == question_id, questions))
        question.order = len(questions) - index - 1

    return True
