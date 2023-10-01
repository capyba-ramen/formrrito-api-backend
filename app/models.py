from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(50))
    created_at = Column(DateTime, nullable=True)
    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    content = Column(String(200), index=True)
    created_at = Column(DateTime, nullable=True)
    deadline = Column(DateTime, nullable=True)
    start_at = Column(DateTime, nullable=True)
    finish_at = Column(DateTime, nullable=True)
    checked = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="todos")
