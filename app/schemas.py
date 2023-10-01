from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Todo(BaseModel):
    title: str
    created_at: Optional[datetime] = None


class UserBase(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    todos: List[Todo]
