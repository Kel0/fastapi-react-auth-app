from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from pydantic.generics import GenericModel

MSG = TypeVar("MSG")


@dataclass
class MetaDataArgs:
    username: str
    email: str
    code: str


@dataclass
class MetaData:
    task: str
    args: MetaDataArgs

    @staticmethod
    def fill(**kwargs):
        return MetaData(task=kwargs["task"], args=MetaDataArgs(**kwargs["args"]))


class APIResponse(GenericModel, Generic[MSG]):
    msg: MSG
    error: Optional[str] = None

    class Config:
        orm_mode = True
