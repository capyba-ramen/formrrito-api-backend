from fastapi import APIRouter, Depends, Query, Body, Path
from sqlalchemy.orm import Session

from app import auth
from app.main import get_db
from . import actions, schemas
from api_form import schemas as form_schemas

router = APIRouter()


@router.get(
    "/{form_id}",
    description="取得單筆表單資料",
    response_model=form_schemas.FormOut
)
def get_form(
        form_id: str = Path(..., title="表單代碼"),
        db: Session = Depends(get_db)
):
    result = actions.get_form(form_id=form_id, db=db)
    return result


@router.post(
    "/{form_id}",
    description="回覆表單",
    response_model=bool
)
def reply(
        form_id: str = Path(..., title="表單代碼"),
        reply_content: schemas.ReplyIn = Body(..., description="回覆內容"),
        db: Session = Depends(get_db)
):
    result = actions.reply(
        form_id=form_id,
        reply_content=reply_content,
        db=db
    )
    return result


@router.get(
    "/statistics/{form_id}",
    description="回覆統計資訊",
    response_model=schemas.StatisticsOut
)
def get_statistics(
        form_id: str = Path(..., title="表單代碼"),
        db: Session = Depends(get_db)
):
    result = actions.get_form(form_id=form_id, db=db)
    return result
