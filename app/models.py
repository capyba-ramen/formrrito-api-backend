import datetime
import uuid

from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import relationship

from api_form.constants import QuestionType
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
    description = Column(String(150), comment="表單描述")
    image_url = Column(String(150), comment="圖片網址")
    accepts_reply = Column(Boolean, default=True, comment="是否接受回覆")
    created_at = Column(DateTime, default=datetime.datetime.now)
    opened_at = Column(DateTime, default=datetime.datetime.now)
    questions = relationship("Question", cascade="all, delete",
                             order_by="Question.created_at.asc(), Question.order.asc()")


class Question(Base):
    __tablename__ = "question"

    id = Column(String(40), primary_key=True, default=uuid.uuid4)
    form_id = Column(String(40), ForeignKey("form.id"))
    title = Column(String(50), comment="問題名稱")
    description = Column(String(150), comment="問題描述")
    type = Column(Integer, default=QuestionType.SIMPLE.value, comment="問題類型")
    is_required = Column(Boolean, default=False, comment="是否為必填")
    image_url = Column(String(150), comment="圖片網址")
    order = Column(Integer, nullable=False, comment="問題順序(排序用)")
    created_at = Column(DateTime, default=datetime.datetime.now)
    options = relationship("Option", cascade="all, delete", order_by="Option.id")


class Option(Base):
    __tablename__ = "option"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(String(40), ForeignKey("question.id"))
    title = Column(String(50), comment="選項名稱")
    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)


class Reply(Base):
    __tablename__ = "reply"

    id = Column(String(40), primary_key=True, default=uuid.uuid4)
    individual_id = Column(String(40), nullable=False, comment="答覆者ID")
    question_id = Column(String(40), ForeignKey("question.id"), nullable=False)
    option_id = Column(String(500), comment="問題是選擇題時才有值")
    response = Column(String(500), comment="回覆(簡答/詳答的答案 & 選擇題的選項)")
    created_at = Column(DateTime, default=datetime.datetime.now)
