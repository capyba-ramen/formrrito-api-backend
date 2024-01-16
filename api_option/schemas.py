from typing import List

from pydantic import BaseModel, Field


class CreateOptionsIn(BaseModel):
    options: List[str] = Field(..., description="選項標題")


class UpdateOptionIn(BaseModel):
    option_id: int = Field(..., description="表單代碼")
    title: str = Field(None, description="問題名稱")
