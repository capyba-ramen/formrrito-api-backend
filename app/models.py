import datetime
import uuid

from api_form.constants import QuestionType
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    ForeignKey
)
from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String(40), primary_key=True, default=uuid.uuid4)
    username = Column(String(50))
    email = Column(String(100), unique=True)
    hashed_password = Column(String(100))
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)


class Form(Base):
    __tablename__ = "form"

    id = Column(String(40), primary_key=True, default=uuid.uuid4)
    user_id = Column(String(40), ForeignKey("user.id"))
    title = Column(String(50), comment="表單名稱")
    description = Column(String(150), nullable=True, comment="表單描述")
    accepts_reply = Column(Boolean, nullable=True, default=True, comment="是否接受回覆")
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)
    opened_at = Column(DateTime, nullable=True, default=datetime.datetime.now)


class Question(Base):
    __tablename__ = "question"

    id = Column(String(40), primary_key=True, default=uuid.uuid4)
    form_id = Column(String(40), ForeignKey("form.id"))
    title = Column(String(50), comment="問題名稱")
    description = Column(String(150), nullable=True, comment="問題描述")
    type = Column(Integer, default=QuestionType.SIMPLE.value, comment="問題類型")
    is_required = Column(Boolean, default=False, comment="是否為必填")
    image_url = Column(String(150), nullable=True, comment="圖片網址")
    order = Column(Integer, comment="問題順序(排序用)")
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)


class Option(Base):
    __tablename__ = "option"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(String(40), ForeignKey("question.id"))
    title = Column(String(50), comment="選項名稱")
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)


class Reply(Base):
    __tablename__ = "reply"

    id = Column(String(40), primary_key=True, default=uuid.uuid4)
    individual_id = Column(String(40), comment="答覆者ID")
    question_id = Column(String(40), ForeignKey("question.id"))
    option_id = Column(Integer, ForeignKey("option.id"))
    answer = Column(String(150), unique=True, comment="簡答/詳答的回覆")
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)
