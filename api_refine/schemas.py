from typing import List

from pydantic import BaseModel, Field


class RefineQuestionTitleIn(BaseModel):
    form_title: str = Field(..., description="表單名稱")
    form_description: str = Field(..., description="表單敘述")
    question_title: str = Field(..., description="問題名稱")


class RefineQuestionDescriptionIn(BaseModel):
    form_title: str = Field(..., description="表單名稱")
    form_description: str = Field(..., description="表單敘述")
    question_title: str = Field(..., description="問題名稱")
    question_description: str = Field(..., description="問題敘述")


class RefineOptionsIn(BaseModel):
    question_title: str = Field(..., description="問題名稱")
    current_options: List[str] = Field([], description="選項資訊")
