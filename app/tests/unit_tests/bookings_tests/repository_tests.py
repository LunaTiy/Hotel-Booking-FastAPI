from datetime import datetime

import pytest

from app.bookings.models import Booking
from app.bookings.repository import BookingRepository


@pytest.mark.parametrize(
    ("room_id", "user_id", "date_from", "date_to"),
    [
        (5, 2, "2020-03-11", "2020-03-18"),
        (6, 2, "2020-03-11", "2020-03-18"),
        (7, 2, "2020-03-11", "2020-03-18"),
        (8, 2, "2020-03-11", "2020-03-18"),
    ]
)
async def test_add_booking(
        room_id: int,
        user_id: int,
        date_from: str,
        date_to: str
) -> None:
    date_from_date = datetime.strptime(date_from, "%Y-%m-%d")
    date_to_date = datetime.strptime(date_to, "%Y-%m-%d")

    booking = await BookingRepository.add(user_id, room_id, date_from_date, date_to_date)
    assert booking

    booking_from_db = await BookingRepository.find_one_or_none(Booking.id == booking.id)
    assert booking_from_db == booking

    await BookingRepository.remove(Booking.id == booking.id)

    booking_from_db = await BookingRepository.find_one_or_none(Booking.id == booking.id)
    assert not booking_from_db
