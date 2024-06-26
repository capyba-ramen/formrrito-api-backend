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
    "image_url": "default/1.webp",
    "questions": [
        {
            "title": "What is your name?",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": False,
            "order": 6,
            "options": []
        },
        {
            "title": "Can you attend?",
            "description": "",
            "type": QuestionType.SINGLE.value,
            "is_required": True,
            "order": 5,
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
            "order": 4,
            "options": []
        },
        {
            "title": "What will you be bringing?",
            "description": "Let us know what kind of dishes you will be bringing to the party.",
            "type": QuestionType.MULTIPLE.value,
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
            "order": 2,
            "options": []
        },
        {
            "title": "Do you have any questions for us?",
            "description": "",
            "type": QuestionType.COMPLEX.value,
            "is_required": False,
            "order": 1,
            "options": []
        },
        {
            "title": "What is your email address?",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": False,
            "order": 0,
            "options": []
        }
    ]
}

contact_information = {
    "title": "Contact Information",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed et faucibus lorem.",
    "image_url": "default/2.webp",
    "questions": [
        {
            "title": "Name",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": True,
            "order": 4,
            "options": []
        },
        {
            "title": "Email",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": True,
            "order": 3,
            "options": []
        },
        {
            "title": "Address",
            "description": "",
            "type": QuestionType.COMPLEX.value,
            "is_required": True,
            "order": 2,
            "options": []
        },
        {
            "title": "Phone Number",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": False,
            "order": 1,
            "options": []
        },
        {
            "title": "Comments",
            "description": "",
            "type": QuestionType.COMPLEX.value,
            "is_required": False,
            "order": 0,
            "options": []
        }
    ]
}

event_registration = {
    "title": "Event Registration",
    "description": "Event Timing: January 5th, 2024\nEvent Address: 123 Y Street Y City, ST 123\nContact us at: 123-456-7890 or mymail@example.com",
    "image_url": "default/3.webp",
    "questions": [
        {
            "title": "Name",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": True,
            "order": 5,
            "options": []
        },
        {
            "title": "Email",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": True,
            "order": 4,
            "options": []
        },
        {
            "title": "Organization",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": True,
            "order": 3,
            "options": []
        },
        {
            "title": "What days will you attend?",
            "description": "",
            "type": QuestionType.MULTIPLE.value,
            "is_required": True,
            "order": 2,
            "options": [
                "Day 1",
                "Day 2",
                "Day 3"
            ]
        },
        {
            "title": "Dietary restrictions",
            "description": "",
            "type": QuestionType.SINGLE.value,
            "is_required": True,
            "order": 1,
            "options": [
                "None",
                "Vegetarian",
                "Vegan",
                "Gluten-free"
                "Kosher",
            ]
        },
        {
            "title": "I understand I'll have to pay $$ upon arrival",
            "description": "",
            "type": QuestionType.SINGLE.value,
            "is_required": True,
            "order": 0,
            "options": [
                "Yes"
            ]
        }
    ]
}

rsvp = {
    "title": "Event RSVP",
    "description": "Event Address: 123 Y Street Y City, ST 123\nContact us at: 123-456-7890 or mymail@example.com",
    "image_url": "default/4.webp",
    "questions": [
        {
            "title": "Can you attend?",
            "description": "",
            "type": QuestionType.SINGLE.value,
            "is_required": True,
            "order": 3,
            "options": [
                "Yes, I will be there!",
                "Sorry, I can't make it."
            ]
        },
        {
            "title": "What are the names of people attending?",
            "description": "",
            "type": QuestionType.COMPLEX.value,
            "is_required": False,
            "order": 2,
            "options": []
        },
        {
            "title": "How did you hear about this event?",
            "description": "",
            "type": QuestionType.MULTIPLE.value,
            "is_required": False,
            "order": 1,
            "options": [
                "Website",
                "Friend",
                "Newsletter",
                "Advertisement"
            ]
        },
        {
            "title": "Comments and/or questions",
            "description": "",
            "type": QuestionType.COMPLEX.value,
            "is_required": False,
            "order": 0,
            "options": []
        }
    ]
}

customer_feedback = {
    "title": "Customer Feedback",
    "description": "We would love to hear your feedback on how we can improve your experience.",
    "image_url": "default/5.webp",
    "questions": [
        {
            "title": "Feedback Type",
            "description": "",
            "type": QuestionType.SINGLE.value,
            "is_required": False,
            "order": 4,
            "options": [
                "Comments",
                "Questions",
                "Bug Reports",
                "Feature Requests"
            ]
        },
        {
            "title": "Feedback",
            "description": "",
            "type": QuestionType.COMPLEX.value,
            "is_required": True,
            "order": 3,
            "options": []
        },
        {
            "title": "Suggestions for improvement",
            "description": "",
            "type": QuestionType.COMPLEX.value,
            "is_required": False,
            "order": 2,
            "options": []
        },
        {
            "title": "Name",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": False,
            "order": 1,
            "options": []
        },
        {
            "title": "Email",
            "description": "",
            "type": QuestionType.SIMPLE.value,
            "is_required": False,
            "order": 0,
            "options": []
        }
    ]
}


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
