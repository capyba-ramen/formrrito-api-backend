from pydantic import BaseModel, Field


class UpdateFormIn(BaseModel):
    form_id: str = Field(..., description="表單代碼")
    field: str = Field(..., description="欄位名稱")
    value: str = Field(..., description="欄位值")
