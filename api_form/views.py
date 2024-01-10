from app import auth
from app.main import get_db
from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from . import actions, schemas

router = APIRouter()


# TODO: 表單列表
@router.get(
    "/list",
    description="表單列表"
)
def get_forms(
        user=Depends(auth.get_current_user),
        start: int = Query(0, title="從第幾筆資料開始"),
        size: int = Query(10, title="一次撈回幾筆資料"),
        sort: str = Query("asc", title="排序方式"),
        db: Session = Depends(get_db)
):
    result = actions.get_forms(user.user_id, start, size, sort, db)
    return result


@router.post(
    "/",
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
    return result


@router.put(
    "/",
    description="修改表單"
)
def update_form(
        user=Depends(auth.get_current_user),
        inputs: schemas.UpdateFormIn = Body(..., title="表單修改資料"),
        db: Session = Depends(get_db)
):
    print(inputs)

    result = actions.update_form(
        user_id=user.user_id,
        inputs=inputs,
        db=db
    )
    return result
