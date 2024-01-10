from pydantic import BaseModel, Field


class UserBaseIn(BaseModel):
    username: str = Field(..., description="使用者名稱")
    password: str = Field(..., description="密碼")
    email: str = Field(..., description="電子郵件")


class UserBaseOut(BaseModel):
    id: str = Field(..., description="使用者代碼")
    username: str = Field(..., description="使用者名稱")
    email: str = Field(..., description="電子郵件")
