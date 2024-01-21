from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api_form import crud as form_crud
from api_form.constants import QuestionType
from api_question import crud as question_crud
from components.db_decorators import transaction
from . import crud, schemas


@transaction
def create_options(
        user_id: str,
        form_id: str,
        question_id: str,
        options: List[schemas.OptionIn],
        db: Session
):
    # 驗證使用者是否有權限修改表單
    form = form_crud.get_form_by_id(form_id, db)
    if form is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="表單不存在"
        )

    if form.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限修改表單"
        )

    question = question_crud.get_question_by_id(
        question_id=question_id,
        form_id=form_id,
        db=db
    )

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="問題不存在"
        )

    # 帶入的 question 不需要選項
    if question.type in [
        QuestionType.SIMPLE.value,
        QuestionType.COMPLEX.value
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="此問題類型不需要選項"
        )

    # ========== 以下開始分三種情況處理選項的新增/刪除/修改 ==========
    existing_options = crud.get_options_by_question_id(
        question_id=question_id,
        db=db
    )
    existing_option_map = {str(option.id): option for option in existing_options}

    for option in options:
        # 新增
        if not option.id:
            print(f"新增選項: {option.title}")
            crud.create_options(
                question_id=question_id,
                titles=[option.title],
                db=db
            )
        # 修改 or 不動
        elif option.id in existing_option_map:
            # 修改
            if option.title != existing_option_map[option.id].title:
                print(f"修改選項(id: {option.id}):{option.title}")
                crud.update_option(
                    option=existing_option_map[option.id],
                    title=option.title
                )
            # 不動
            else:
                print(f"不動選項(id: {option.id}):{option.title}")

            existing_option_map.pop(option.id, None)  # 從 map 中移除

    print(f"TO BE DELETED: {existing_option_map}")
    # 刪除 map 中剩下的選項 (沒有從 body 帶入的表示要刪除)
    for existing_option in existing_option_map.values():
        print(f"刪除選項(id: {existing_option.id}):{existing_option.title}")
        crud.delete_option(
            option=existing_option,
            db=db
        )

    return True
