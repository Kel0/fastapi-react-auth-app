from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from clubhouse.models import User
from settings import ALGORITHM, SECRET_KEY

from .schemas import DecodedToken

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login/access-token")


def get_current_user(token: str = Security(reusable_oauth2)):
    auth_handler = AuthHandler()
    try:
        payload = auth_handler.decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(detail="Could not validate credentials", status_code=403)

    user = User.find(payload.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


class AuthHandler:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = SECRET_KEY
    algorithm = ALGORITHM

    def authenticate_user(self, username: str, password):
        user = User.get_user(username=username)
        if user is None:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def verify_token(self, token, user_id):
        decoded_token = self.decode_token(token)

        if datetime.fromtimestamp(decoded_token.exp) < datetime.utcnow():
            return False
        if decoded_token.sub != user_id:
            return False
        return True

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=self.algorithm)
            return DecodedToken(**payload)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
