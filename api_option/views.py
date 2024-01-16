from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from app import auth
from app.main import get_db
from . import actions, schemas

router = APIRouter()


@router.post(
    "/{form_id}/{question_id}",
    response_model=bool,
    description="新增選項 (單筆/多筆)"
)
def create_options(
        user=Depends(auth.get_current_user),
        form_id: str = Path(..., title="表單編號"),
        question_id: str = Path(..., title="問題編號"),
        inputs: schemas.CreateOptionsIn = Body(..., title="選項資訊"),
        db: Session = Depends(get_db)
):
    result = actions.create_options(
        user_id=user.user_id,
        form_id=form_id,
        question_id=question_id,
        options=inputs.options,
        db=db
    )
    return result


@router.put(
    "/{form_id}/{question_id}",
    response_model=bool,
    description="編輯單筆"
)
def update_option(
        user=Depends(auth.get_current_user),
        form_id: str = Path(..., title="表單編號"),
        question_id: str = Path(..., title="問題編號"),
        inputs: schemas.UpdateOptionIn = Body(..., title="選項資訊"),
        db: Session = Depends(get_db)
):
    result = actions.update_option(
        user_id=user.user_id,
        form_id=form_id,
        question_id=question_id,
        inputs=inputs,
        db=db
    )
    return result


@router.delete(
    "/{form_id}/{question_id}/{option_id}",
    response_model=bool,
    description="刪除單筆問題"
)
def delete_option(
        user=Depends(auth.get_current_user),
        form_id: str = Path(..., title="表單代碼"),
        question_id: str = Path(..., title="問題代碼"),
        option_id: str = Path(..., title="選項代碼"),
        db: Session = Depends(get_db)
):
    result = actions.delete_option(
        user_id=user.user_id,
        form_id=form_id,
        question_id=question_id,
        option_id=option_id,
        db=db
    )
    return result
