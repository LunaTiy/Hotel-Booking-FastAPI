from fastapi import APIRouter, HTTPException

from app.users.auth import get_password_hash
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import SchemeUserRegister

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и Пользователи"]
)


@router.post("/register")
async def register_user(user_data: SchemeUserRegister):
    existing_user = await UserRepository.find_one_or_none(User.email == user_data.email)

    if existing_user:
        raise HTTPException(status_code=500)

    hashed_password = get_password_hash(user_data.password)
    await UserRepository.add(email=user_data.email, hashed_password=hashed_password)
