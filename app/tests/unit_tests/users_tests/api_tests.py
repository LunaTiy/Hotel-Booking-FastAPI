import pytest
from httpx import AsyncClient
from pydantic import EmailStr


@pytest.mark.parametrize(
    ("email", "password", "status_code"),
    [
        ("kot@pes.com", "kotopes", 200),
        ("kot@pes.com", "kot0pes", 409),
        ("pes@cot.com", "kot0pes", 200),
        ("qwerty", "kot0pes", 422),
    ]
)
async def test_register_user(
        email: EmailStr,
        password: str,
        status_code: int,
        async_client: AsyncClient
) -> None:
    response = await async_client.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize(
    ("email", "password", "status_code"),
    [
        ("test@test.com", "test", 200),
        ("daniil@example.com", "artem", 200),
        ("not_known@example.com", "artem", 401),
        ("some_test", "test", 422),
    ]
)
async def test_login_user(
        email: EmailStr,
        password: str,
        status_code: int,
        async_client: AsyncClient
) -> None:
    response = await async_client.post("/auth/login", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code
