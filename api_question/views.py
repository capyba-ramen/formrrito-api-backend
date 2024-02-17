from typing import Union

from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session

from api_form.schemas import OptionOut
from app import auth
from app.main import get_db
from components.aws_s3_service import s3_copy_object, s3_delete_object
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


@router.post(
    "/{form_id}/{question_id}",
    response_model=schemas.CreateQuestionOut,
    description="複製單筆問題"
)
async def duplicate_question(
        user=Depends(auth.get_current_user),
        form_id: str = Path(..., title="表單編號"),
        question_id: str = Path(..., title="問題編號"),
        db: Session = Depends(get_db)
):
    new_added_question_id, old_image_url, new_image_url = actions.duplicate_question(
        user_id=user.user_id,
        form_id=form_id,
        question_id=question_id,
        db=db
    )

    # 複製一份圖片
    if old_image_url:
        await s3_copy_object(copy_source=old_image_url, new_key=new_image_url)

    return schemas.CreateQuestionOut(
        question_id=new_added_question_id
    )


@router.put(
    "/",
    response_model=Union[OptionOut, None],  #
    description="編輯單筆問題"
)
async def update_question(
        user=Depends(auth.get_current_user),
        inputs: schemas.UpdateQuestionIn = Body(..., title="問題資訊"),
        db: Session = Depends(get_db)
):
    existing_image_url, deletes_s3_by_image_url, permanent_image_url = (
        await actions.upload_question_image_before_update_question(
            form_id=inputs.form_id,
            question_id=inputs.question_id,
            input_image_url=inputs.image_url,
            db=db
        )
    )

    inputs.image_url = permanent_image_url
    result = actions.update_question(
        user_id=user.user_id,
        inputs=inputs,
        db=db
    )

    # 刪除舊的圖片
    if deletes_s3_by_image_url:
        if existing_image_url and existing_image_url[:7] != 'default':
            await s3_delete_object(object_name=existing_image_url)
    return result


@router.delete(
    "/{form_id}/{question_id}",
    response_model=bool,
    description="刪除單筆問題"
)
async def delete_question(
        user=Depends(auth.get_current_user),
        form_id: str = Path(..., title="表單代碼"),
        question_id: str = Path(..., title="問題代碼"),
        db: Session = Depends(get_db)
):
    result, image_url = actions.delete_question(
        user_id=user.user_id,
        form_id=form_id,
        question_id=question_id,
        db=db
    )

    # 刪除圖片
    if image_url and image_url[:7] != 'default':
        await s3_delete_object(object_name=image_url)

    return result
