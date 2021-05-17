from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class DecodedToken:
    iat: int
    exp: int
    sub: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class BaseUser(BaseModel):
    email: str
    username: str


class CreateUser(BaseUser):
    password: str


class UserTokenPayload(BaseUser):
    token: str


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True
