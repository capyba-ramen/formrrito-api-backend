from pydantic import BaseModel, Field


class UrlIn(BaseModel):
    url: str = Field(..., description="網址")


class EmailIn(BaseModel):
    subject: str = Field(..., description="主旨")
    to: str = Field(..., description="收件者")
