import smtplib
from email.message import EmailMessage

from environmemt import EMAIL_HOST, SERVICE_EMAIL, SERVICE_EMAIL_PASSWORD


def send_email(subject: str, to: str):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_HOST
    msg['To'] = to
    # TODO: implement html template for email
    content = ">You got 1 response! Check {here}! "

    msg.set_content(content)

    # send email
    with smtplib.SMTP_SSL(EMAIL_HOST, 465) as smtp:
        smtp.login(SERVICE_EMAIL, SERVICE_EMAIL_PASSWORD)
        smtp.send_message(msg)
