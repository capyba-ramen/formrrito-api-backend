from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api_form import crud as form_crud
from api_question import crud as question_crud
from components.aws_s3_service import s3_upload_object
from components.email import send_email, render_template
from . import crud
from .schemas import EmailIn


def get_original_url(
        shortened_url: str,
        db: Session
) -> str:
    original_url = crud.get_original_url(
        shortened_url=shortened_url,
        db=db
    )
    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="網址不存在"
        )
    return original_url.link


def get_shortened_url(
        url: str,
        db: Session
) -> str:
    shortened_url = crud.get_shortened_url_by_link(
        link=url,
        db=db
    )
    if shortened_url:
        return shortened_url.key
    shortened_url = crud.create_shortened_url(
        url=url,
        db=db
    )
    return shortened_url


def dev_send_email(
        inputs: EmailIn
) -> bool:
    data = {
        'form': "HI capybaramen~~~~~",
        'form_link': 'http://localhost:3333/form/897eafbf-0430-47ef-83f9-f9198779674e#responses'
    }
    html = render_template('default.j2', data=data)
    send_email(
        subject=inputs.subject,
        to=inputs.to,
        body=html
    )

    return True


async def upload_image(
        inputs,
        file,
        db: Session
) -> bool:
    """
    此 action 用用於上傳圖片，用於表單或問題

    note: 1. 資料驗證待優化 2. 非同步 & 更新 DB 之流程中錯誤處理待優化
    """
    # TODO: upload_type 驗證移動到 schemas
    if inputs.upload_type not in ["form", "question"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="upload_type 參數錯誤"
        )

    # 驗證 form or question 是否存在
    form = form_crud.get_form_by_id(
        form_id=inputs.form_id,
        db=db
    )
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="表單不存在"
        )

    question = question_crud.get_question_by_id(
        question_id=inputs.question_id,
        form_id=inputs.form_id,
        db=db
    )

    if inputs.upload_type == "question" and not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="問題不存在"
        )

    supported_file_types = {
        'image/png': 'png',
        'image/jpeg': 'jpg'
    }
    if file.content_type not in supported_file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支援的檔案格式"
        )

    contents = await file.read()
    upload_result = await s3_upload_object(
        contents=contents,
        object_name="{}.{}".format(
            inputs.form_id if inputs.upload_type == "form" else inputs.question_id,
            supported_file_types[file.content_type]
        ),
        content_type=file.content_type
    )

    # 上傳成功，更新 DB
    if upload_result:
        if inputs.upload_type == "form":
            form_crud.update_form_image_url(
                form=form,
                image_url=f"{inputs.form_id}.{supported_file_types[file.content_type]}",
                db=db
            )
        else:
            question_crud.update_image_url(
                question=question,
                image_url=f"{inputs.question_id}.{supported_file_types[file.content_type]}",
                db=db
            )

    return upload_result
