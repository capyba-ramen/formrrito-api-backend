from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Todo(BaseModel):
    title: str
    created_at: Optional[datetime]


class UserBaseIn(BaseModel):
    username: str
    password: str
    email: str


class UserBaseOut(BaseModel):
    id: str
    username: str
    email: Optional[str]
