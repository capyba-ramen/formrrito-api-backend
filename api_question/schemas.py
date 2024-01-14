from pydantic import BaseModel, Field


class CreateQuestionOut(BaseModel):
    question_id: str = Field(..., description="問題代碼")
