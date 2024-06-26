from typing import List

from pydantic import BaseModel, Field


class CreateQuestionOut(BaseModel):
    question_id: str = Field(..., description="問題代碼")


class UpdateQuestionIn(BaseModel):
    form_id: str = Field(..., description="表單代碼")
    question_id: str = Field(..., description="問題代碼")
    title: str = Field(None, description="問題名稱")
    description: str = Field(None, description="問題描述")
    type: int = Field(..., description="問題類型")
    is_required: bool = Field(None, description="問題是否必填")
    image_url: str = Field(None, description="問題圖片網址")


class DeleteQuestionIn(BaseModel):
    form_id: str = Field(..., description="表單代碼")
    question_id: str = Field(..., description="問題代碼")


class ChangeQuestionOrderIn(BaseModel):
    form_id: str = Field(..., description="表單代碼")
    question_ids_in_order: List[str] = Field(..., description="問題代碼列表依照順序排列")
