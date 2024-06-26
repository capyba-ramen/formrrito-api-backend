import uuid
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session, joinedload

from app.models import Form, Question
from components.db_decorators import transaction


def get_form_by_id(form_id: str, db: Session):
    form = db.query(Form).filter(Form.id == form_id).first()
    return form


def get_form_detail_by_id(form_id: str, db: Session):
    # together with questions and options
    form = db.query(Form).options(
        joinedload(Form.questions).joinedload(Question.options)
    ).filter(Form.id == form_id).first()
    return form


def get_forms_by_user_query(user_id: str, db: Session):
    return db.query(Form).filter(
        Form.user_id == user_id
    )


def get_forms_by_user_with_order_and_size(user_id: str, start: int, size: int, sort, db: Session):
    order = Form.opened_at.asc() if sort == 'asc' else Form.opened_at.desc()

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

    data = form_query_with_conditions.all()

    return data


def create_form(
        user_id: str,
        db: Session,
        title: str = None,
        description: str = None,
        image_url: str = None,
):
    form_id = str(uuid.uuid4())
    form = Form(
        id=form_id,
        user_id=user_id
    )
    if title:
        form.title = title
    if description:
        form.description = description
    if image_url:
        form.image_url = image_url
    db.add(form)
    return form_id


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
    elif field == 'image_url':
        form.image_url = value
    return True


@transaction
def update_form_opened_at(
        form: Form,
        db: Session
):
    form.opened_at = datetime.utcnow()
    return form


def delete_form(
        form: Form,
        db: Session
):
    db.delete(form)
    return True


@transaction
def update_form_image_url(
        form: Form,
        image_url: str,
        db: Session
):
    form.image_url = image_url
    return True
