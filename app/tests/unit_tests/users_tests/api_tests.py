import pytest
from httpx import AsyncClient
from pydantic import EmailStr


@pytest.mark.parametrize(
    "email, password, status_code",
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
):
    response = await async_client.post("/auth/register", json={
        "email": email,
        "password": password,
    })

    assert response.status_code == status_code
