from pydantic import BaseModel, Field


class CreateQuestionOut(BaseModel):
    question_id: str = Field(..., description="問題代碼")


class UpdateQuestionIn(BaseModel):
    form_id: str = Field(..., description="表單代碼")
    question_id: str = Field(..., description="問題代碼")
    title: str = Field(None, description="問題名稱")
    description: str = Field(None, description="問題描述")
    type: int = Field(None, description="問題類型")
    is_required: bool = Field(None, description="問題是否必填")


class DeleteQuestionIn(BaseModel):
    form_id: str = Field(..., description="表單代碼")
    question_id: str = Field(..., description="問題代碼")
