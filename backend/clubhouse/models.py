from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy_mixins import AllFeaturesMixin, TimestampsMixin

from .database import JsonType, base, engine, session


class BaseModel(base, AllFeaturesMixin, TimestampsMixin):
    __abstract__ = True

    id = Column(Integer, autoincrement=True, primary_key=True)

    def __init__(self, *args, **kwargs):
        pass


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(length=14), unique=True)
    username = Column(String(length=255), unique=True)
    hashed_password = Column(Text, default=None)
    confirmed = Column(Boolean, default=False)
    code = Column(Text, default=None)

    @classmethod
    def get_user(cls, username: str):
        results = cls.where(username=username).all()
        return results[0] if len(results) else None

    @classmethod
    def get_or_create(cls, username: str, email: str, code: str):
        user = cls.get_user(username=username)

        if user is None:
            user = cls.create(username=username, email=email, code=code)
            return user, True

        return user, False


class Task(BaseModel):
    __tablename__ = "tasks"

    meta = Column(JsonType, default={})


base.metadata.create_all(engine)
BaseModel.set_session(session)
