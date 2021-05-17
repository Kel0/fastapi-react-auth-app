from fastapi import APIRouter

from .auth.api import users

v1 = APIRouter()
v1.include_router(users, prefix="/users")
