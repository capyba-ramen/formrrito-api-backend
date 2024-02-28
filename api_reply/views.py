from fastapi import APIRouter, Depends, Body, Path, BackgroundTasks
from sqlalchemy.orm import Session

from api_form import schemas as form_schemas
from app import auth
from app.main import get_db
from components.email import send_email, render_template
from environmemt import WEB_URL
from . import actions, schemas

router = APIRouter()


@router.post(
    "/responses",
    description="匯出表單回覆",
    response_model=str  # pre-signed_url
)
async def export_responses(
        user=Depends(auth.get_current_user),
        inputs: schemas.ExportResponsesIn = Body(..., title="表單代碼"),
        db: Session = Depends(get_db)
):
    result = await actions.export_responses(
        form_id=inputs.form_id,
        db=db
    )
    return result


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
        background_tasks: BackgroundTasks,
        form_id: str = Path(..., title="表單代碼"),
        reply_content: schemas.ReplyIn = Body(..., description="回覆內容"),
        db: Session = Depends(get_db)
):
    result, form_title, form_owner_email, form_owner_username = actions.reply(
        form_id=form_id,
        reply_content=reply_content,
        db=db
    )

    # 如果成功，就寄信給表單所有者
    if result:
        data = {
            "form_title": form_title,
            "form_link": f"{WEB_URL}/form/{form_id}#responses",
            "user_name": form_owner_username,
        }
        html = render_template('default.j2', data=data)
        background_tasks.add_task(
            send_email,
            subject="You've Got a Response on Formrrito! 📝",
            to=form_owner_email,
            body=html
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
    result = actions.get_statistics(form_id=form_id, db=db)
    return result
