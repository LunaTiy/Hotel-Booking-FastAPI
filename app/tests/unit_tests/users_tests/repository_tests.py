import pytest
from pydantic import EmailStr

from app.users.models import User
from app.users.repository import UserRepository


@pytest.mark.parametrize(
    ("user_id", "email", "is_exists"),
    [
        (1, "test@test.com", True),
        (2, "daniil@example.com", True),
        (10, "not_exists", False)
    ]
)
async def test_find_user_by_id(
        user_id: int,
        email: EmailStr,
        is_exists: bool
) -> None:
    user = await UserRepository.find_one_or_none(User.id == user_id)

    if is_exists:
        assert user
        assert user.email == email
        assert user.id == user_id
    else:
        assert not user
