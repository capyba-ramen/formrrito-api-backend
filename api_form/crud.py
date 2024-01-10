from typing import Any

from app.models import Form
from components.paginator import paginate_data
from sqlalchemy.orm import Session


def get_form_by_id(form_id: str, db: Session):
    form = db.query(Form).filter(Form.id == form_id).first()
    return form


def get_forms(user_id: str, start: int, size: int, sort, db: Session):
    order = Form.opened_at.asc() if sort == 'ASC' else Form.opened_at.desc()

    form_query = db.query(Form).filter(
        Form.user_id == user_id
    )
    form_query_with_conditions = form_query.order_by(
        order
    ).offset(
        start - 1
    ).limit(
        size + 1  # 多撈一筆判斷是否有下一頁!!
    )

    return paginate_data(
        form_query,
        form_query_with_conditions,
        start,
        size
    )


def create_form(
        user_id: str,
        db: Session
):
    form = Form(
        user_id=user_id
    )
    db.add(form)
    return True


def update_form(
        form: Form,
        field: str,
        value: Any
):
    if field == 'title':
        form.title = value
    elif field == 'description':
        form.description = value
    elif field == 'accepts_reply':
        form.accepts_reply = value
    return True
