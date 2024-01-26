import random

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api_option import crud as option_crud
from api_question import crud as question_crud
from components.db_decorators import transaction
from components.paginator import paginate_data
from . import crud, schemas
from .constants import CustomForm, custom_form_template_map


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
                    image_url=form.image_url if form.image_url else "",
                    description=form.description if form.description else "",
                    accepts_reply=form.accepts_reply,
                    created_at=form.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                    opened_at=form.opened_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
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
        image_url=form.image_url if form.image_url else "",
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
                order=question.order,
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
        user_id=user_id,
        db=db,
        image_url=str(random.randint(1, 10))
    )
    print(f"Successfully created form (id:{result})")
    return result


@transaction
def create_custom_form(
        user_id: str,
        template: str,
        db: Session
):
    """
    建立客製化表單
    表單有 5 種類型
    1. PARTY_INVITE (派對邀請)
    2. CONTACT_INFORMATION (聯絡資訊)
    3. EVENT_REGISTRATION (活動報名)
    4. RSVP (回覆邀請)
    5. CUSTOMER_FEEDBACK (客戶回饋)
    """

    if template not in [
        CustomForm.PARTY_INVITE.value,
        CustomForm.CONTACT_INFORMATION.value,
        CustomForm.EVENT_REGISTRATION.value,
        CustomForm.RSVP.value,
        CustomForm.CUSTOMER_FEEDBACK.value
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="表單模板類型不存在"
        )

    template_data = custom_form_template_map[template]
    # 建立表單
    form_id = crud.create_form(
        user_id=user_id,
        db=db,
        title=template_data['title'],
        description=template_data['description'],
        image_url=template_data['image_url']
    )

    # 建立問題
    for question in template_data['questions']:
        question_id = question_crud.create_question(
            form_id=form_id,
            db=db,
            title=question['title'],
            description=question['description'],
            question_type=question['type'],
            is_required=question['is_required'],
            order=question['order']
        )

        # 建立選項
        option_crud.create_options(
            question_id=question_id,
            db=db,
            titles=question['options']
        )

    return form_id


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
