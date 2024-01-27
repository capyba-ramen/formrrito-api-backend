from pydantic import BaseModel, Field


class UrlIn(BaseModel):
    url: str = Field(..., description="網址")
