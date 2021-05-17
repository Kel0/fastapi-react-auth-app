import logging
from datetime import datetime, timedelta
from typing import Callable, List, Union

from celery import Celery

from settings import (
    ENV,
    HOST_EMAIL,
    HOST_PWD,
    SMTP_HOST,
    SMTP_PORT,
    CeleryConfig,
    CeleryConfigDocker,
)

from .auth.mailer import Message, Server
from .auth.utils import AuthHandler
from .models import Task, User
from .schemas import MetaData

logger = logging.getLogger(__name__)


app = Celery("tasks")
app.config_from_object(CeleryConfig if ENV == "local" else CeleryConfigDocker)
auth_handler = AuthHandler()


class TaskManager:
    @staticmethod
    def register_task(task: Union[str, Callable], args: dict):
        schema = {"task": task if not callable(task) else task.__name__, "args": args}
        return Task.create(meta=schema)

    @staticmethod
    def get_tasks():
        return Task.all()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(minutes=15), clean_users.s(), name="Clean auth every 15min"
    )
    sender.add_periodic_task(timedelta(seconds=10), send_mail.s(), name="Send mails")


@app.task(name="sendMails")
def send_mail():
    logger.info("SEND MAILS TASK IS RUNNING")
    _tasks: List[Task] = TaskManager.get_tasks()

    for _task in _tasks:
        meta_data = MetaData.fill(**_task.meta)

        if meta_data.task != "send_mail":
            continue

        logger.info(f"HANDLING TASK {_task.id}")
        session = Server(host=SMTP_HOST, port=SMTP_PORT)
        session.login(HOST_EMAIL, HOST_PWD)
        msg = Message.create(
            from_email=HOST_EMAIL,
            to_email=meta_data.args.email,
            to_username=meta_data.args.username,
            subject="Authenticate confirmation",
            content=meta_data.args.code,
        )
        Message.send(msg, session=session)
        logger.info(f"MESSAGE HAS BEEN SENT TO {meta_data.args.email}")
        _task.delete()


@app.task(name="cleanTrashUsers")
def clean_users():
    _users: List[User] = User.all()

    for _user in _users:
        if _user.confirmed:
            continue

        jwt_decoded = auth_handler.decode_token(_user.code)

        if datetime.fromtimestamp(jwt_decoded.exp) < datetime.utcnow():
            logger.info(f"USER {_user.email} HAS BEEN DELETED")
            _user.delete()
