from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api_form import crud as form_crud
from components.db_decorators import transaction
from . import crud


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
