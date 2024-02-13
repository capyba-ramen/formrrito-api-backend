from fastapi import Form
from pydantic import BaseModel, Field


class UrlIn(BaseModel):
    url: str = Field(..., description="網址")


class EmailIn(BaseModel):
    subject: str = Field(..., description="主旨")
    to: str = Field(..., description="收件者")


class UploadImageInForm(BaseModel):
    """
    reference: https://stackoverflow.com/questions/60127234/how-to-use-a-pydantic-model-with-form-data-in-fastapi
    """
    upload_type: str
    form_id: str
    question_id: str = None

    @classmethod
    def as_form(
            cls,
            upload_type: str = Form(...),
            form_id: str = Form(...),
            question_id: str = Form(None)
    ):
        return cls(
            upload_type=upload_type,
            form_id=form_id,
            question_id=question_id
        )


class DeleteImageIn(BaseModel):
    delete_type: str
    form_id: str
    question_id: str = None
    image_url: str
