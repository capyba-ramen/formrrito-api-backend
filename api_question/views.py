from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app import auth
from app.main import get_db
from . import actions, schemas

router = APIRouter()


@router.post(
    "/{form_id}",
    response_model=schemas.CreateQuestionOut,
    description="新增單筆問題"
)
def create_question(
        user=Depends(auth.get_current_user),
        form_id: str = Path(..., title="表單編號"),
        db: Session = Depends(get_db)
):
    result = actions.create_question(
        user_id=user.user_id,
        form_id=form_id,
        db=db
    )
    return schemas.CreateQuestionOut(
        question_id=result
    )
