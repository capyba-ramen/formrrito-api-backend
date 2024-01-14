from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api_form import crud as form_crud
from api_form.constants import QuestionType
from components.db_decorators import transaction
from . import crud, schemas


@transaction
def create_question(
        user_id: str,
        form_id: str,
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

    result = crud.create_question(
        form_id=form_id,
        db=db
    )

    return result


@transaction
def update_question(
        user_id: str,
        inputs: schemas.UpdateQuestionIn,
        db: Session
):
    # 驗證使用者是否有權限
    form = form_crud.get_form_by_id(inputs.form_id, db)

    if form is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="表單不存在"
        )

    if form.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限修改問題"
        )

    question = crud.get_question_by_id(inputs.question_id, db)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="問題不存在"
        )

    if inputs.type is not None and inputs.type not in [
        QuestionType.SIMPLE.value,
        QuestionType.COMPLEX.value,
        QuestionType.SINGLE.value,
        QuestionType.MULTIPLE.value,
        QuestionType.DROP_DOWN.value,
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="問題類型錯誤"
        )

    result = crud.update_question(
        question=question,
        fields=inputs,
    )

    return result


@transaction
def delete_question(
        user_id: str,
        form_id: str,
        question_id: str,
        db: Session
):
    # 驗證使用者是否有權限
    form = form_crud.get_form_by_id(form_id, db)

    if form is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="表單不存在"
        )

    if form.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限修改問題"
        )

    question = crud.get_question_by_id(question_id, db)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="問題不存在"
        )

    result = crud.delete_question(
        question=question,
        db=db
    )

    return result
