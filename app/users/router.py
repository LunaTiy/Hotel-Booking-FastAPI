from fastapi import APIRouter, Response, Depends

from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPassword
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.repository import UserRepository
from app.users.schemas import SchemeUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и Пользователи"]
)


@router.post("/register")
async def register_user(user_data: SchemeUserAuth):
    existing_user = await UserRepository.find_one_or_none(User.email == user_data.email)

    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UserRepository.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SchemeUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)

    if not user:
        raise IncorrectEmailOrPassword

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user
