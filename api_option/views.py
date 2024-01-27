from typing import List

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from api_form.schemas import OptionOut
from app import auth
from app.main import get_db
from . import actions, schemas, crud

router = APIRouter()


@router.post(
    "/{form_id}/{question_id}",
    response_model=List[OptionOut],
    description="新增選項 (單筆/多筆), 編輯選項, 以及刪除選項"
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
    # 增刪改成功，回傳所有選項
    if result:
        options = crud.get_options_by_question_id(
            question_id=question_id,
            db=db
        )

        return [
            OptionOut(
                id=option.id,
                title=option.title
            ) for option in options
        ]
