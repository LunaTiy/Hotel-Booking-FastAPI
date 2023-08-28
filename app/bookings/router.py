from fastapi import APIRouter

from app.bookings.repository import BookingRepository

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def get_bookings():
    return await BookingRepository.find_all()


@router.get("/{booking_id}")
def get_booking(booking_id: int):
    pass
