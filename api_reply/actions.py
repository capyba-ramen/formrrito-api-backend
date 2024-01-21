import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from components.db_decorators import transaction

from . import schemas, crud
from api_form import crud as form_crud, schemas as form_schemas
from api_form.constants import QuestionType
from api_question import crud as question_crud


def get_form(
        form_id: str,
        db: Session
):
    form = form_crud.get_form_detail_by_id(form_id, db)

    if form is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="表單不存在"
        )

    return form_schemas.FormOut(
        id=form.id,
        title=form.title if form.title else "",
        image_url=form.image_url if form.image_url else "",
        description=form.description if form.description else "",
        accepts_reply=form.accepts_reply,
        created_at=form.created_at,
        opened_at=form.opened_at,
        questions=[
            form_schemas.QuestionOut(
                id=question.id,
                title=question.title if question.title else "",
                description=question.description if question.description else "",
                type=question.type,
                is_required=question.is_required,
                order=question.order,
                options=[
                    form_schemas.OptionOut(
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
def reply(
        form_id: str,
        reply_content: schemas.ReplyIn,
        db: Session
):
    form = form_crud.get_form_detail_by_id(form_id, db)

    if form is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="表單不存在"
        )

    if not form.accepts_reply:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="表單不接受回覆"
        )

    questions = question_crud.get_questions_with_options_by_form_id(form_id, db)

    questions_map = {question.id: question for question in questions}

    is_required_question_id_map = {
        question.id: 1
        for question in questions if question.is_required
    }
    print(is_required_question_id_map)

    individual_id = str(uuid.uuid4())

    for single_reply in reply_content.replies:

        question_replied_to = questions_map.get(single_reply.question_id)

        if not question_replied_to:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"問題不存在<question_id={single_reply.question_id}>"
            )

        if single_reply.question_type != question_replied_to.type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"問題類型已改變, 請重新整理<question_id={single_reply.question_id}>"
            )

        # 簡答題或詳答題
        if question_replied_to.type in [
            QuestionType.SIMPLE.value,
            QuestionType.COMPLEX.value
        ]:

            if single_reply.answer:
                crud.create_reply(
                    individual_id=individual_id,
                    question_id=question_replied_to.id,
                    response=single_reply.answer,
                    db=db,
                )
                # 移除必填問題
                print("答覆簡答")
                is_required_question_id_map.pop(question_replied_to.id, None)
                print("移除必填問題", is_required_question_id_map)

        # 單選題、多選題、下拉題
        elif question_replied_to.type in [
            QuestionType.SINGLE.value,
            QuestionType.MULTIPLE.value,
            QuestionType.DROP_DOWN.value,
        ]:
            if not single_reply.option_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"選項未填<option_id={single_reply.option_id}>"
                )

            if int(single_reply.option_id) not in [
                option.id for option in question_replied_to.options
            ]:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"選項不存在<option_id={single_reply.option_id}>"
                )

            crud.create_reply(
                individual_id=individual_id,
                question_id=question_replied_to.id,
                response=single_reply.option_title,
                db=db,
                option_id=single_reply.option_id,
            )
            # 移除必填問題
            is_required_question_id_map.pop(question_replied_to.id, None)
            print("答覆選擇題")
            print("移除必填問題", is_required_question_id_map)
            print(is_required_question_id_map)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"問題類型錯誤<question_id:{single_reply.question_id}, question_type={single_reply.question_type}>"
            )

    # TODO: 處理必填未填的問題
    if is_required_question_id_map:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"必填問題未填<question_ids={list(is_required_question_id_map.keys())}>"
        )
    return True


def get_statistics(
        form_id: str,
        db: Session
):
    pass
