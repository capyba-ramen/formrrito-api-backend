from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from components.db_decorators import transaction
from components.paginator import paginate_data
from . import crud, schemas


def get_forms(
        user_id: str,
        start: int,
        size: int,
        sort: str,
        db: Session
):
    if start <= 0 or size <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start 或 size 不可小於 0"
        )
    forms = crud.get_forms_by_user_with_order_and_size(user_id, start, size, sort, db)

    def transform_data(orm):
        transformed_result = []
        for form in orm:
            transformed_result.append(
                schemas.FormBaseOut(
                    id=form.id,
                    title=form.title if form.title else "",
                    description=form.description if form.description else "",
                    accepts_reply=form.accepts_reply,
                    created_at=form.created_at,
                    opened_at=form.opened_at
                )
            )
        return transformed_result

    result = paginate_data(
        crud.get_forms_by_user_query(user_id, db),
        forms,
        transform_data,
        start,
        size
    )

    return result


def get_form(
        user_id: str,
        form_id: str,
        db: Session
):
    form = crud.get_form_detail_by_id(form_id, db)

    if form is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="表單不存在"
        )

    if form.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限瀏覽表單"
        )

    crud.update_form_opened_at(form=form, db=db)  # 更新表格開啟時間

    return schemas.FormOut(
        id=form.id,
        title=form.title if form.title else "",
        description=form.description if form.description else "",
        accepts_reply=form.accepts_reply,
        created_at=form.created_at,
        opened_at=form.opened_at,
        questions=[
            schemas.QuestionOut(
                id=question.id,
                title=question.title if question.title else "",
                description=question.description if question.description else "",
                type=question.type,
                is_required=question.is_required,
                options=[
                    schemas.OptionOut(
                        id=option.id,
                        title=option.title
                    )
                    for option in question.options
                ]
            )
            for question in form.questions
        ]
    )


@transaction
def create_form(
        user_id: str,
        db: Session
):
    result = crud.create_form(
        user_id=user_id, db=db
    )
    print(f"Successfully created form (id:{result})")
    return result


@transaction
def update_form(
        user_id: str,
        inputs: schemas.UpdateFormIn,
        db: Session
):
    # 驗證使用者是否有權限修改表單
    form = crud.get_form_by_id(inputs.form_id, db)

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

    if inputs.field not in [
        'title',
        'description',
        'accepts_reply'
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{inputs.field} 欄位不存在"
        )

    result = crud.update_form(
        form=form,
        field=inputs.field,
        value=inputs.value
    )
    return result


@transaction
def delete_form(
        user_id: str,
        form_id: str,
        db: Session
):
    # 驗證使用者是否有權限刪除表單
    form = crud.get_form_by_id(form_id, db)

    if form is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="表單不存在"
        )

    if form.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="無權限刪除表單"
        )

    result = crud.delete_form(
        form=form,
        db=db
    )

    return result
