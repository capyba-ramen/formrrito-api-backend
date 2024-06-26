from typing import List

from pydantic import BaseModel, Field


class OptionIn(BaseModel):
    id: str = Field(..., description="選項代碼")
    title: str = Field(..., description="選項名稱")


class CreateOptionsIn(BaseModel):
    options: List[OptionIn] = Field(..., description="選項列表")



