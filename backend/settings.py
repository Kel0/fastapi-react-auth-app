from decouple import config

from pathlib import Path


ABS_PATH = Path().resolve()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = config("DATABASE_URL", cast=str)
SECRET_KEY = config("SECRET_KEY", cast=str)
SMTP_HOST = config("SMTP_HOST", cast=str)
SMTP_PORT = config("SMTP_PORT", cast=int)
HOST_EMAIL = config("HOST_EMAIL", cast=str)
HOST_PWD = config("HOST_PWD", cast=str)
ENV = config("ENV", cast=str, default="local")


class CeleryConfig:
    broker_url = "redis://localhost"
    backend = "redis://localhost"
    RESULT_BACKEND = "redis://localhost"
    ACCEPT_CONTENT = ["application/json"]
    RESULT_SERIALIZER = "json"
    TASK_SERIALIZER = "json"
    TIMEZONE = "Asia/Almaty"


class CeleryConfigDocker:
    broker_url = "redis://redis:6379/0"
    backend = "redis://redis:6379/0"
    RESULT_BACKEND = "redis://redis:6379/0"
    ACCEPT_CONTENT = ["application/json"]
    RESULT_SERIALIZER = "json"
    TASK_SERIALIZER = "json"
    TIMEZONE = "Asia/Almaty"
    BEAT_SCHEDULE = {
        "amount-counting": {
            "task": "profile.tasks.amount_counting",
            "schedule": 60.0,
        },
    }

