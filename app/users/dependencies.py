import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from app.users.models import User
from app.users.repository import UserRepository


def get_token(request: Request) -> str:
    token: str = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        payload = jwt.decode(token, settings.secret_key, settings.secret_algo)
    except JWTError:
        raise IncorrectTokenFormatException from None

    expire: str = payload.get("exp")

    if not expire or int(expire) < datetime.datetime.now(datetime.UTC).timestamp():
        raise TokenExpiredException

    user_id: str = payload.get("sub")

    if not user_id:
        raise UserIsNotPresentException

    user = await UserRepository.find_one_or_none(User.id == int(user_id))

    if not user:
        raise UserIsNotPresentException

    return user
