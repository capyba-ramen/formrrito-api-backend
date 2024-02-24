from typing import List

from fastapi import APIRouter, Depends, Body

from app import auth
from . import actions, schemas

router = APIRouter()


@router.post(
    "/question/title",
    response_model=str,
    description="潤飾問題標題"
)
def refine_question_title(
        user=Depends(auth.get_current_user),
        inputs: schemas.RefineQuestionTitleIn = Body(..., title="潤飾問題標題需提供的資訊"),
):
    result = actions.refine_question_title(
        form_title=inputs.form_title,
        form_description=inputs.form_description,
        question_title=inputs.question_title
    )
    return result


@router.post(
    "/question/description",
    response_model=str,
    description="潤飾問題敘述"
)
def refine_question_description(
        user=Depends(auth.get_current_user),
        inputs: schemas.RefineQuestionDescriptionIn = Body(..., title="潤飾問題敘述需提供的資訊"),
):
    result = actions.refine_question_description(
        form_title=inputs.form_title,
        form_description=inputs.form_description,
        question_title=inputs.question_title,
        question_description=inputs.question_description
    )
    return result


@router.post(
    "/question/options",
    response_model=List[str],
    description="推薦選項"
)
def refine_options(
        user=Depends(auth.get_current_user),
        inputs: schemas.RefineOptionsIn = Body(..., title="推薦選項需提供的資訊"),
):
    result = actions.refine_options(
        question_title=inputs.question_title,
        current_options=inputs.current_options
    )
    return result
