from datetime import datetime

from fastapi import Request, Depends
from jose import jwt, JWTError

from app.config import settings
from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenFormatException, UserIsNotPresent
from app.users.models import User
from app.users.repository import UserRepository


def get_token(request: Request) -> str:
    token: str = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_KEY, settings.JWT_ALGO)
    except JWTError:
        raise IncorrectTokenFormatException

    expire: str = payload.get("exp")

    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException

    user_id: str = payload.get("sub")

    if not user_id:
        raise UserIsNotPresent

    user = await UserRepository.find_one_or_none(User.id == int(user_id))

    if not user:
        raise UserIsNotPresent

    return user
