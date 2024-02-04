import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from environmemt import EMAIL_HOST, SERVICE_EMAIL, SERVICE_EMAIL_PASSWORD


def render_template(template, **kwargs):
    """
    renders a Jinja template into HTML
    """
    # check if template exists
    template_path = os.path.join("templates", template)

    if not os.path.exists(template_path):
        print('No template file present: %s' % template)
        return None

    import jinja2
    template_loader = jinja2.FileSystemLoader(searchpath="templates")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template(template)
    return template.render(**kwargs)


def send_email(subject: str, to: str, body=None):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_HOST
    msg['To'] = to
    msg.attach(MIMEText(body, 'html'))

    # send email
    try:
        with smtplib.SMTP_SSL(EMAIL_HOST, 465) as smtp:
            smtp.login(SERVICE_EMAIL, SERVICE_EMAIL_PASSWORD)
            smtp.sendmail(SERVICE_EMAIL, to, msg.as_string())
    except Exception as e:
        print("Error sending email")
        print(e)
        return False
