from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from app import auth
from app.main import get_db
from . import actions, schemas

router = APIRouter()


@router.post(
    "/order",
    response_model=bool,
    description="調整問題順序"
)
def change_order(
        user=Depends(auth.get_current_user),
        inputs: schemas.ChangeQuestionOrderIn = Body(...),
        db: Session = Depends(get_db)
):
    result = actions.change_order(
        user_id=user.user_id,
        inputs=inputs,
        db=db
    )
    return result


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


@router.put(
    "/",
    response_model=int,  #
    description="編輯單筆問題"
)
def update_question(
        user=Depends(auth.get_current_user),
        inputs: schemas.UpdateQuestionIn = Body(..., title="問題資訊"),
        db: Session = Depends(get_db)
):
    result = actions.update_question(
        user_id=user.user_id,
        inputs=inputs,
        db=db
    )
    return result


@router.delete(
    "/{form_id}/{question_id}",
    response_model=bool,
    description="刪除單筆問題"
)
def delete_question(
        user=Depends(auth.get_current_user),
        form_id: str = Path(..., title="表單代碼"),
        question_id: str = Path(..., title="問題代碼"),
        db: Session = Depends(get_db)
):
    result = actions.delete_question(
        user_id=user.user_id,
        form_id=form_id,
        question_id=question_id,
        db=db
    )
    return result
