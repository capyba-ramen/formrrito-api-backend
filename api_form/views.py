from fastapi import APIRouter, Depends, Query, Body, Path
from sqlalchemy.orm import Session

from app import auth
from app.main import get_db
from . import actions, schemas

router = APIRouter()


@router.get(
    "/list",
    description="表單列表"
)
def get_forms(
        user=Depends(auth.get_current_user),
        start: int = Query(1, title="從第幾筆資料開始"),
        size: int = Query(10, title="一次撈回幾筆資料"),
        sort: str = Query("asc", title="排序方式"),
        db: Session = Depends(get_db)
):
    result = actions.get_forms(user.user_id, start, size, sort, db)
    return result


@router.get(
    "/{form_id}",
    description="取得單筆表單資料"
)
def get_form(
        user=Depends(auth.get_current_user),
        form_id: str = Path(..., title="表單代碼"),
        db: Session = Depends(get_db)
):
    result = actions.get_form(user_id=user.user_id, form_id=form_id, db=db)
    return result


@router.post(
    "/",
    response_model=schemas.CreateFormOut,
    description="新增表單"
)
def create_form(
        user=Depends(auth.get_current_user),
        db: Session = Depends(get_db)
):
    result = actions.create_form(
        user_id=user.user_id,
        db=db
    )
    return schemas.CreateFormOut(
        form_id=result
    )


@router.put(
    "/",
    description="修改表單"
)
def update_form(
        user=Depends(auth.get_current_user),
        inputs: schemas.UpdateFormIn = Body(..., title="表單修改資料"),
        db: Session = Depends(get_db)
):
    result = actions.update_form(
        user_id=user.user_id,
        inputs=inputs,
        db=db
    )
    return result


@router.delete(
    "/{form_id}",
    description="刪除表單"
)
def delete_form(
        user=Depends(auth.get_current_user),
        form_id: str = Path(..., title="表單代碼"),
        db: Session = Depends(get_db)
):
    result = actions.delete_form(
        user_id=user.user_id,
        form_id=form_id,
        db=db
    )
    return result
