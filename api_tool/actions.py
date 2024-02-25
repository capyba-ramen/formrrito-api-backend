import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api_form import crud as form_crud
from api_question import crud as question_crud
from components.aws_s3_service import s3_upload_object, s3_delete_object, s3_list_objects
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
):
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
    # 驗證格式 & 大小
    supported_file_types = {
        'image/png': 'png',
        'image/jpeg': 'jpg'
    }
    size_limit = 1024 * 1024 * 5  # 5MB

    if file.content_type not in supported_file_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支援的檔案格式"
        )

    contents = await file.read()

    if not 0 < len(contents) <= size_limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Supported file size is 0 - 5 MB'
        )

    # 以 form_id 為資料夾區分各表單圖片
    image_url_id = f"{form.id}/{str(uuid.uuid4())}" if inputs.upload_type == "form" else f"{form.id}/_{str(uuid.uuid4())}"
    upload_result = await s3_upload_object(
        contents=contents,
        object_name="{}.{}".format(
            image_url_id,
            supported_file_types[file.content_type]
        ),
        content_type=file.content_type
    )

    # 上傳成功，更新 DB
    if upload_result:
        if inputs.upload_type == "form":
            # 把舊的圖片刪除
            if form.image_url and form.image_url[:7] != 'default':
                await s3_delete_object(
                    object_name=form.image_url
                )
            # form 的 image_url 直接更新至 DB
            form_crud.update_form_image_url(
                form=form,
                image_url=f"{image_url_id}.{supported_file_types[file.content_type]}",
                db=db
            )

        else:  # question 的 image_url 不直接更新至 DB (在 PUT /api/question 時再更新，並把舊圖刪除)
            pass
            # question_crud.update_image_url(
            #     question=question,
            #     image_url=f"{image_url_id}.{supported_file_types[file.content_type]}",
            #     db=db
            # )
    # 上傳失敗
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="圖片上傳失敗"
        )

    return upload_result if not upload_result else f"{image_url_id}.{supported_file_types[file.content_type]}"


async def delete_image(
        inputs,
        db: Session
):
    # TODO: upload_type 驗證移動到 schemas
    if inputs.delete_type not in ["form", "question"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="delete_type 參數錯誤"
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

    if inputs.delete_type == "question" and not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="問題不存在"
        )

    if inputs.delete_type == "form":
        if form.image_url != inputs.image_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="image_url 參數錯誤"
            )
    else:
        if question.image_url != inputs.image_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="image_url 參數錯誤"
            )

    # 刪除 S3 上的圖片
    delete_image_result = await s3_delete_object(
        object_name=inputs.image_url
    )

    # 刪除成功，更新 DB
    if delete_image_result:
        if inputs.delete_type == "form":
            form_crud.update_form_image_url(
                form=form,
                image_url="",
                db=db
            )
        else:  # question 的 image_url 不直接更新至 DB (在 PUT /api/question 時再更新)
            pass
            # question_crud.update_image_url(
            #     question=question,
            #     image_url="",
            #     db=db
            # )

    return delete_image_result


async def delete_objects_by_folder(
        folder_name: str
):
    objects = s3_list_objects(prefix=f"{folder_name}/")
    for obj in objects:
        await s3_delete_object(object_name=obj['Key'])
