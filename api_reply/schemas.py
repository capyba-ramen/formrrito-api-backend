from typing import List, Union

from pydantic import BaseModel, Field


class SingleReply(BaseModel):
    question_id: str = Field(..., description="問題代碼")
    question_type: int = Field(..., description="問題類型")
    option_ids: List[str] = Field(None, description="選項代碼列表(選擇的選項的 id, 如是簡答題或詳答題則 null)")
    option_titles: List[str] = Field(None, description="選項名稱列表(選擇的選項的名稱, 如是簡答題或詳答題則 null)")
    answer: str = Field(None, description="回答內容(簡答題或詳答題才有)")


class ReplyIn(BaseModel):
    replies: List[SingleReply] = Field(..., description="回覆列表")


class QuestionStatisticBaseOut(BaseModel):
    title: str = Field(..., description="問題標題")
    count: int = Field(..., description="回覆數")
    type: int = Field(..., description="問題種類(決定圖表類型)")
    is_required: bool = Field(..., description="是否必填")


class QuestionStatisticTextOut(QuestionStatisticBaseOut):
    responses: List[str] = Field(..., description="回答內容(簡答題或詳答題)")


class OptionStatisticOut(BaseModel):
    title: str = Field(..., description="選項名稱")
    count: int = Field(..., description="回覆數")


class QuestionStatisticChoiceOut(QuestionStatisticBaseOut):
    options: List[OptionStatisticOut] = Field(..., description="回答內容(問題為選項類型<單選/多選/下拉式>)")


class StatisticsOut(BaseModel):
    total: int = Field(..., description="總回覆數")
    accepts_reply: bool = Field(..., description="是否接受回覆")
    questions: List[Union[QuestionStatisticTextOut, QuestionStatisticChoiceOut]] = Field(..., description="問題列表")
