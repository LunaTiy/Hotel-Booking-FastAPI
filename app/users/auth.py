from datetime import datetime, timedelta
from typing import Dict, Optional

from jose import jwt
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from pydantic import EmailStr

from app.config import settings
from app.users.models import User
from app.users.repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_KEY, settings.JWT_ALGO)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str) -> Optional[User]:
    user: User = await UserRepository.find_one_or_none(User.email == email)

    if user and verify_password(password, user.hashed_password):
        return user
