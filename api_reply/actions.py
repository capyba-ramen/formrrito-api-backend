import uuid

import pandas as pd
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from api_form import crud as form_crud, schemas as form_schemas
from api_form.constants import QuestionType
from api_question import crud as question_crud
from components.aws_s3_service import s3_upload_object, create_presigned_url
from components.db_decorators import transaction
from components.pandas_utils import convert_df_to_excel
from . import schemas, crud


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
        created_at=form.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
        opened_at=form.opened_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
        questions=[
            form_schemas.QuestionOut(
                id=question.id,
                title=question.title if question.title else "",
                description=question.description if question.description else "",
                type=question.type,
                is_required=question.is_required,
                image_url=question.image_url if question.image_url else "",
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
            status_code=status.HTTP_403_FORBIDDEN,
            detail="表單不接受回覆"
        )

    questions = question_crud.get_questions_with_options_by_form_id(form_id, db)

    questions_map = {question.id: question for question in questions}

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
            # 問題必填但未提供答案
            if question_replied_to.is_required and not single_reply.answer:
                raise HTTPException(
                    status_code=status.HTTP_418_IM_A_TEAPOT,
                    detail=f"{question_replied_to.title}"
                )

            # 問題不是必填但沒有給答案
            if not single_reply.answer:
                continue

            crud.create_reply(
                individual_id=individual_id,
                question_id=question_replied_to.id,
                response=single_reply.answer,
                db=db,
            )

        # 單選題、多選題、下拉題
        elif question_replied_to.type in [
            QuestionType.SINGLE.value,
            QuestionType.MULTIPLE.value,
            QuestionType.DROP_DOWN.value,
        ]:
            # 問題必填但未提供選項
            if question_replied_to.is_required and not single_reply.option_titles:
                raise HTTPException(
                    status_code=status.HTTP_418_IM_A_TEAPOT,
                    detail=f"{question_replied_to.title}"
                )

            # 問題不是必填但沒有給選項
            if not single_reply.option_titles:
                continue

            if set(single_reply.option_ids) - set([
                str(option.id) for option in question_replied_to.options
            ]):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"選項不存在<option_ids={single_reply.option_ids}>"
                )

            crud.create_reply(
                individual_id=individual_id,
                question_id=question_replied_to.id,
                response=",".join(single_reply.option_titles),
                db=db,
                option_id=",".join(single_reply.option_ids)
            )

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"問題類型錯誤<question_id:{single_reply.question_id}, question_type={single_reply.question_type}>"
            )

    return True, form.title, form.user.email, form.user.username


def get_statistics(
        form_id: str,
        db: Session
):
    # 驗證表單是否存在
    form = form_crud.get_form_by_id(form_id, db)
    if form is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="表單不存在"
        )

    questions = question_crud.get_questions_by_form_id(form_id, db)
    question_ids = [question.id for question in questions]
    question_map = {question.id: question for question in questions}

    replies = crud.get_replies_by_question_ids(question_ids, db)

    question_statistics_map = {}

    for single_reply in replies:
        if question_map.get(single_reply.question_id).type in [
            QuestionType.SIMPLE.value,
            QuestionType.COMPLEX.value
        ]:

            if single_reply.question_id not in question_statistics_map:
                question_statistics_map[single_reply.question_id] = schemas.QuestionStatisticTextOut(
                    title=question_map.get(single_reply.question_id).title if question_map.get(
                        single_reply.question_id).title else "",
                    count=0,
                    type=question_map.get(single_reply.question_id).type,
                    is_required=question_map.get(single_reply.question_id).is_required,
                    responses=[]
                )
            question_statistics_map[single_reply.question_id].count += 1
            question_statistics_map[single_reply.question_id].responses.append(single_reply.response)

        elif question_map.get(single_reply.question_id).type in [
            QuestionType.SINGLE.value,
            QuestionType.MULTIPLE.value,
            QuestionType.DROP_DOWN.value,
        ]:
            if single_reply.question_id not in question_statistics_map:
                question_statistics_map[single_reply.question_id] = {
                    "title": question_map.get(single_reply.question_id).title if question_map.get(
                        single_reply.question_id).title else "",
                    "count": 0,
                    "type": question_map.get(single_reply.question_id).type,
                    "is_required": question_map.get(single_reply.question_id).is_required,
                    "options": {}
                }
            question_statistics_map[single_reply.question_id]["count"] += 1
            option_titles = single_reply.response.split(",")
            for option_title in option_titles:
                if option_title not in question_statistics_map[single_reply.question_id]["options"]:
                    question_statistics_map[single_reply.question_id]["options"][option_title] = 0
                question_statistics_map[single_reply.question_id]["options"][option_title] += 1

    question_stats = []
    for question_id in question_ids:
        # 判斷此問題有沒有被回答到
        question_stat = question_statistics_map.get(question_id)
        if not question_stat:
            continue

        if question_map.get(question_id).type in [
            QuestionType.SIMPLE.value,
            QuestionType.COMPLEX.value
        ]:
            question_stats.append(question_stat)

        elif question_map.get(question_id).type in [
            QuestionType.SINGLE.value,
            QuestionType.MULTIPLE.value,
            QuestionType.DROP_DOWN.value,
        ]:
            question_stats.append(
                schemas.QuestionStatisticChoiceOut(
                    title=question_stat["title"],
                    count=question_stat["count"],
                    type=question_stat["type"],
                    is_required=question_stat["is_required"],
                    options=[
                        schemas.OptionStatisticOut(
                            title=option_title,
                            count=question_stat["options"][option_title]
                        )
                        for option_title in question_stat["options"]
                    ]
                )
            )
    # number of responses
    individuals = set([per_reply.individual_id for per_reply in replies])

    return schemas.StatisticsOut(
        total=len(individuals),
        accepts_reply=form.accepts_reply,
        question_stats=question_stats
    )


async def export_responses(
        form_id: str,
        db: Session
):
    form = form_crud.get_form_by_id(form_id, db)
    if form is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="表單不存在"
        )

    # 1.1 撈出 questions
    questions = question_crud.get_questions_by_form_id(form_id, db)
    question_ids = [question.id for question in questions]  # 已照順序
    question_ids.insert(0, 'response_time')

    # 1.2 撈出所有回覆 by individual
    replies = crud.get_replies_by_question_ids(question_ids, db)

    # 1.3 generate a list of objects
    # where object like {individual_id: {question_id_1: response_1, question_id_2: response_2, ...}}
    individual_responses = {}
    for single_reply in replies:
        if single_reply.individual_id not in individual_responses:
            individual_responses[single_reply.individual_id] = {}
        individual_responses[single_reply.individual_id][single_reply.question_id] = single_reply.response
        individual_responses[single_reply.individual_id]['response_time'] = single_reply.created_at.strftime(
            '%Y-%m-%d %H:%M:%S')

    # prepare individual_responses according to questions as columns
    data_list = []
    for individual_response in individual_responses.values():
        data_list.append(tuple(individual_response.get(question_id, "") for question_id in question_ids))

    # 1.4 prepare columns but add 'Response Time to the first column'
    columns = [question.title for question in questions]
    columns.insert(0, 'Response Time (UTC)')

    # 2. 產生 excel & put object to s3
    # columns = ['id', 'name', 'age']
    # data_list = [
    #     (1, 'John', 25),
    #     (2, 'Jane', 30),
    #     (3, 'Bob', 22)
    # ]
    df = pd.DataFrame(data_list, columns=columns)
    excel_data = convert_df_to_excel(df)
    object_name = f"{form_id}/{form.title}.xlsx"
    await s3_upload_object(
        contents=excel_data,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        object_name=object_name
    )

    # 3. generate pre-signed url
    pre_signed_url = await create_presigned_url(
        object_name=object_name
    )

    if not pre_signed_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="無法產生 pre-signed url"
        )

    return pre_signed_url
