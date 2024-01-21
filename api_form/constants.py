import enum


class QuestionType(enum.IntEnum):
    SIMPLE = 0  # 簡答
    COMPLEX = 1  # 詳答
    SINGLE = 2  # 單選
    MULTIPLE = 3  # 複選
    DROP_DOWN = 4  # 下拉選單


party_invite = {
    "title": "Party Invite",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed et faucibus lorem.",
    "image_url": "",
    "questions": [
        {
            "title": "What is your name?",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": False,
            "order": 0,
            "options": []
        },
        {
            "title": "Can you attend?",
            "description": "",
            "type": QuestionType.SINGLE.value,
            "is_required": True,
            "order": 1,
            "options": [
                    "Yes, I will be there!",
                    "Sorry, I can't make it."
            ]
        },
        {
            "title": "How many of you are attending?",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": False,
            "order": 2,
            "options": []
        },
        {
            "title": "What will you be bringing?",
            "description": "Let us know what kind of dishes you will be bringing to the party.",
            "type": QuestionType.COMPLEX.value,
            "is_required": False,
            "order": 3,
            "options": [
                "Mains",
                "Salad",
                "Dessert",
                "Drinks",
                "Sides/Appetizers"
            ]
        },
        {
            "title": "Do you have any allergies or dietary restrictions?",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": False,
            "order": 4,
            "options": []
        },
        {
            "title": "Do you have any questions for us?",
            "description": "",
            "type": QuestionType.COMPLEX.value,
            "is_required": False,
            "order": 5,
            "options": []
        },
        {
            "title": "What is your email address?",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": False,
            "order": 6,
            "options": []
        }
    ]
}

# TODO: 這裡要補上其他表單的資訊
contact_information = {}
event_registration = {}
rsvp = {}
customer_feedback = {}


class CustomForm(str, enum.Enum):
    PARTY_INVITE = "party_invite"  # 派對邀請
    CONTACT_INFORMATION = "contact_information"  # 聯絡資訊
    EVENT_REGISTRATION = "event_registration"  # 活動報名
    RSVP = 'rsvp'  # 回覆邀請
    CUSTOMER_FEEDBACK = 'customer_feedback'  # 客戶回饋


custom_form_template_map = {
    CustomForm.PARTY_INVITE.value: party_invite,
    CustomForm.CONTACT_INFORMATION.value: contact_information,
    CustomForm.EVENT_REGISTRATION.value: event_registration,
    CustomForm.RSVP.value: rsvp,
    CustomForm.CUSTOMER_FEEDBACK.value: customer_feedback
}