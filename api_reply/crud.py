from app.models import Reply
from sqlalchemy.orm import Session


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
