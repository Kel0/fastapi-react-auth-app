from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar, Union

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


@dataclass
class CeleryTask:
    name: Union[str, Callable]
    state: bool

    def update_state(self, status):
        self.state = status


class APIResponse(GenericModel, Generic[MSG]):
    msg: MSG
    error: Optional[str] = None

    class Config:
        orm_mode = True
