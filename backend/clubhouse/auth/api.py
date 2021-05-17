from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from clubhouse.models import User
from clubhouse.schemas import APIResponse
from clubhouse.tasks import TaskManager

from .schemas import BaseUser, CreateUser, TokenResponse, UserTokenPayload
from .utils import AuthHandler

users = APIRouter()
auth_handler = AuthHandler()


@users.post("/registration/step-1", response_model=APIResponse[str], tags=["User"])
def user_registration(new_user: BaseUser):
    """
    Create user without password and send email to confirmation
    personality
    """
    token = auth_handler.encode_token(f"{new_user.email}:{new_user.username}")
    user, _status = User.get_or_create(
        username=new_user.username, email=new_user.email, code=token
    )
    if not _status:
        raise HTTPException(detail="User already exists", status_code=400)

    TaskManager.register_task(
        task="send_mail",
        args={
            "username": new_user.username,
            "email": new_user.email,
            "code": token,
        },
    )

    return APIResponse(msg="Send email")


@users.post("/registration/step-2", response_model=APIResponse[str], tags=["User"])
def user_registration_confirmation(new_user: CreateUser):
    """
    Update user's password after confirmation by email
    """
    user: User = User.get_user(username=new_user.username)

    if not user.confirmed:
        raise HTTPException(detail="User's email is not confirmed", status_code=400)

    hashed_password = auth_handler.get_password_hash(new_user.password)
    user.hashed_password = hashed_password
    user.confirmed = True
    user.update()
    return APIResponse(msg="Successfully registered")


@users.post("/email-confirmation", response_model=APIResponse[str], tags=["Email"])
def email_confirmation(new_user: UserTokenPayload):
    """
    User's personality confirmation via email
    """
    user: User = User.get_user(username=new_user.username)

    if user is None:
        raise HTTPException(detail="User is not exist", status_code=400)
    if user.code != new_user.token:
        raise HTTPException(detail="Confirmation token is not correct", status_code=401)
    if user.confirmed:
        raise HTTPException(detail="User already confirmed", status_code=400)

    verified_token_status = auth_handler.verify_token(
        token=user.code, user_id=f"{new_user.email}:{new_user.username}"
    )
    if not verified_token_status:
        raise HTTPException(detail="Confirmation token is not correct", status_code=401)

    user.confirmed = True
    user.update()

    return APIResponse(msg="Success")


@users.post(
    "/login/access-token", response_model=APIResponse[TokenResponse], tags=["User"]
)
def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Generate access token for user
    """
    user = auth_handler.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if user is None:
        raise HTTPException(
            detail="Incorrect username and/or password", status_code=400
        )

    return APIResponse(
        msg=TokenResponse(
            access_token=auth_handler.encode_token(user.id), token_type="bearer"
        )
    )
