import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.parametrize(
    ("room_id", "date_from", "date_to", "booked_rooms", "status_code"),
    [
        (4, "2030-05-01", "2030-05-15", 3, 201),
        (4, "2030-05-02", "2030-05-16", 4, 201),
        (4, "2030-05-03", "2030-05-17", 5, 201),
        (4, "2030-05-04", "2030-05-18", 6, 201),
        (4, "2030-05-05", "2030-05-19", 7, 201),
        (4, "2030-05-06", "2030-05-20", 8, 201),
        (4, "2030-05-07", "2030-05-21", 9, 201),
        (4, "2030-05-08", "2030-05-22", 10, 201),
        (4, "2030-05-09", "2030-05-23", 10, 409),
        (4, "2030-05-10", "2030-05-24", 10, 409),
    ]
)
async def test_add_and_get_booking(
        room_id: int,
        date_from: str,
        date_to: str,
        booked_rooms: int,
        status_code: int,
        authenticated_async_client: AsyncClient
) -> None:
    response = await authenticated_async_client.post("/bookings/add", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    })

    assert response.status_code == status_code

    response = await authenticated_async_client.get("/bookings/")
    assert len(response.json()) == booked_rooms


async def test_get_and_delete_all_bookings(
        authenticated_async_client: AsyncClient
) -> None:
    response = await authenticated_async_client.get("/bookings/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) != 0

    bookings = response.json()

    for booking in bookings:
        booking_id = booking["booking_id"]
        delete_response = await authenticated_async_client.delete(f"/bookings/{booking_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    response = await authenticated_async_client.get("/bookings/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0
