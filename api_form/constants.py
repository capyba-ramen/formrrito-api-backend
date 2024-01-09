import enum


class QuestionType(enum.IntEnum):
    SIMPLE = 0  # 簡答
    COMPLEX = 1  # 詳答
    SINGLE = 2  # 單選
    MULTIPLE = 3  # 複選
    DROP_DOWN = 4  # 下拉選單
   