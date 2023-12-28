import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.parametrize(
    ("location", "date_from", "date_to", "expected_status_code", "expected_hotels_count"),
    [
        ("Республика Алтай", "2020-05-01", "2020-05-15", 200, 3),
        ("Республика Алтай", "2023-05-01", "2023-05-15", 200, 3),
        ("Алтай", "2023-05-01", "2023-05-15", 200, 3),
        ("Коми", "2023-05-01", "2023-05-31", 200, 2),
        ("Сириус", "2023-05-01", "2023-05-31", 200, 1),
        ("Не существует", "2023-05-01", "2023-05-31", 200, 0),
        ("Алтай", "2023-05-01", "2023-04-01", 400, 0),
        ("Алтай", "2023-05-01", "2023-06-01", 400, 0),
        ("Алтай", "2023-0501", "2023-06-01", 422, 0),
    ]
)
async def test_get_hotels_by_location_and_time(
        location: str,
        date_from: str,
        date_to: str,
        expected_status_code: int,
        expected_hotels_count: int,
        async_client: AsyncClient
) -> None:
    response = await async_client.get(f"/hotels/{location}", params={
        "date_from": date_from,
        "date_to": date_to
    })

    assert response.status_code == expected_status_code

    if response.status_code == status.HTTP_200_OK:
        hotels = response.json()
        assert len(hotels) == expected_hotels_count
