from datetime import date

import pytest

from app.bookings.models import Booking
from app.bookings.repository import BookingRepository


@pytest.mark.parametrize(
    ("user_id", "room_id", "date_from", "date_to"),
    [
        (2, 2, date(2023, 7, 10), date(2023, 7, 24)),
        (1, 3, date(2023, 10, 15), date(2023, 10, 29)),
    ]
)
async def test_add_and_get_booking(
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
) -> None:
    new_booking = await BookingRepository.add(user_id, room_id, date_from, date_to)

    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    new_booking = await BookingRepository.find_one_or_none(Booking.id == new_booking.id)

    assert new_booking
