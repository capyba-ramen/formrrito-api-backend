import uuid

from sqlalchemy.orm import Session

from app.models import Question


def create_question(
        form_id: str,
        db: Session
):
    question_id = str(uuid.uuid4())
    question = Question(
        question_id=question_id,
        form_id=form_id,
    )
    db.add(question)
    return form_id
