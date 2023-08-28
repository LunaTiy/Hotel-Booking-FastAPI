from typing import List

from fastapi import APIRouter

from app.bookings.repository import BookingRepository
from app.bookings.schemas import SchemaBooking

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def get_bookings() -> List[SchemaBooking]:
    return await BookingRepository.find_all()


@router.get("/{booking_id}")
def get_booking(booking_id: int):
    pass
