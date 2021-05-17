import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

from settings import ABS_PATH


def _read_template(path):
    with open(path, "r", encoding="utf-8") as f:
        f_content = f.read()
    return Template(f_content)


class Server:
    def __init__(self, host, port):
        self.SMTP = smtplib.SMTP(host=host, port=port)
        self.SMTP.starttls()

    def login(self, email, pwd):
        self.SMTP.login(email, pwd)
        return self

    def send_message(self, msg):
        self.SMTP.send_message(msg)


class Message:
    @staticmethod
    def create(from_email, to_username, to_email, content, subject):
        msg = MIMEMultipart()
        message = _read_template(
            os.path.join(ABS_PATH, "clubhouse/Resources/message.txt")
        ).substitute(PERSON_NAME=to_username, CODE=content)

        msg["From"] = from_email
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        return msg

    @staticmethod
    def send(msg, *, session):
        session.send_message(msg)
