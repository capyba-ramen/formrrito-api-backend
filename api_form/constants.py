import enum


class QuestionType(enum.IntEnum):
    SIMPLE = 0  # 簡答
    COMPLEX = 1  # 詳答
    SINGLE = 2  # 單選
    MULTIPLE = 3  # 複選
    DROP_DOWN = 4  # 下拉選單


party_invite = {
    "title": "派對邀請",
    "description": "派對邀請",
    "questions": [
        {
            "title": "姓名",
            "description": "請填寫您的姓名",
            "type": QuestionType.SIMPLE.value,
            "is_required": True,
            "options": []
        },
        {
            "title": "是否參加",
            "description": "請填寫您是否參加",
            "type": QuestionType.SINGLE.value,
            "is_required": True,
            "options": [
                {
                    "title": "參加"
                },
                {
                    "title": "不參加"
                }
            ]
        },
        {
            "title": "是否攜伴",
            "description": "請填寫您是否攜伴",
            "type": QuestionType.SINGLE.value,
            "is_required": True,
            "options": [
                {
                    "title": "攜伴"
                },
                {
                    "title": "不攜伴"
                }
            ]
        },
        {
            "title": "攜伴姓名",
            "description": "請填寫您攜伴的姓名",
            "type": QuestionType.SIMPLE.value,
            "is_required": False,
            "options": []
        },
        {
            "title": "攜伴是否參加",
            "description": "請填寫您攜伴是否參加",
            "type": QuestionType.SINGLE.value,
            "is_required": False,
            "options": [
                {
                    "title": "參加"
                },
                {
                    "title": "不參加"
                }
            ]
        }
    ]
}


class CustomForm(enum.Enum):
    PARTY_INVITE = party_invite  # 派對邀請
    CONTACT_INFORMATION = 1  # 聯絡資訊
    EVENT_REGISTRATION = 2  # 活動報名
    RSVP = 3  # 回覆邀請
    CUSTOMER_FEEDBACK = 4  # 客戶回饋
