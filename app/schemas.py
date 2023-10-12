from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Todo(BaseModel):
    title: str
    created_at: Optional[datetime]


class UserBaseIn(BaseModel):
    username: str
    email: str


class UserBaseOut(BaseModel):
    id: int
    username: str
    email: Optional[str]
