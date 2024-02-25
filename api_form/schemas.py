from typing import List, Any, Union

from pydantic import BaseModel, Field


class UpdateFormIn(BaseModel):
    form_id: str = Field(..., description="表單代碼")
    field: str = Field(..., description="欄位名稱")
    value: Any = Field(..., description="欄位值")


class CreateFormOut(BaseModel):
    form_id: str = Field(..., description="表單代碼")


class OptionOut(BaseModel):
    id: str = Field(..., description="選項代碼")
    title: str = Field(..., description="選項標題")


class QuestionOut(BaseModel):
    id: str = Field(..., description="題目代碼")
    title: str = Field(..., description="題目標題")
    description: str = Field("None", description="題目描述")
    type: int = Field(..., description="題目類型")
    is_required: bool = Field(..., description="題目是否必填")
    image_url: str = Field("None", description="題目圖片")
    order: int = Field(..., description="題目排序")
    options: List[OptionOut] = Field(None, description="題目選項")


class FormBaseOut(BaseModel):
    id: str = Field(..., description="表單代碼")
    title: str = Field(None, description="表單標題")
    image_url: str = Field(None, description="表單圖片")
    description: str = Field(None, description="表單描述")
    accepts_reply: bool = Field(..., description="表單是否接受回覆")
    created_at: str = Field(..., description="表單建立時間")
    opened_at: str = Field(..., description="表單開放時間")


class FormOut(FormBaseOut):
    questions: List[QuestionOut] = Field(None, description="表單題目")


class UpdateQuestionOut(BaseModel):
    option: Union[OptionOut, None] = Field(..., description="")
    permanent_image_url: str = Field(..., description="永久圖片網址(確定更新問題後的)")
