from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api_form import crud as form_crud
from api_form.constants import QuestionType
from components.db_decorators import transaction
from . import crud, schemas
from api_option import crud as option_crud


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

    question = crud.get_question_by_id(
        question_id=inputs.question_id,
        form_id=inputs.form_id,
        db=db
    )

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

    # 如果問題是選擇題且要把問題類型改成其他類型，則刪除所有選項
    if question.type in [
        QuestionType.SINGLE.value,
        QuestionType.MULTIPLE.value,
        QuestionType.DROP_DOWN.value,
    ] and inputs.type not in [
        QuestionType.SINGLE.value,
        QuestionType.MULTIPLE.value,
        QuestionType.DROP_DOWN.value,
    ]:
        options = option_crud.get_options_by_question_id(
            question_id=question.id,
            db=db
        )

        for option in options:
            option_crud.delete_option(
                option=option,
                db=db
            )

    return True


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

    question = crud.get_question_by_id(
        question_id=question_id,
        form_id=form_id,
        db=db
    )

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


@transaction
def change_order(
        user_id: str,
        inputs: schemas.ChangeQuestionOrderIn,
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
    questions = crud.get_questions_by_form_id(
        form_id=inputs.form_id,
        db=db
    )

    return crud.change_order(
        questions=questions,
        question_order=inputs.question_ids_in_order
    )
