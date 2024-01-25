from typing import List

from sqlalchemy.orm import Session

from app.models import Reply


def create_reply(
        individual_id: str,
        question_id: str,
        response: str,
        db: Session,
        option_id: str = None
):
    reply = Reply(
        individual_id=individual_id,
        question_id=question_id,
        response=response
    )
    if option_id:
        reply.option_id = option_id
    db.add(reply)
    return True


def get_replies_by_question_ids(
        question_ids: List[str],
        db: Session
):
    return db.query(Reply).filter(
        Reply.question_id.in_(question_ids)
    ).all()
