from components.db_decorators import transaction
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
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
    forms = crud.get_forms(user_id, start, size, sort, db)
    return forms


@transaction
def create_form(
        user_id: str,
        db: Session
):
    result = crud.create_form(
        user_id=user_id, db=db
    )
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
