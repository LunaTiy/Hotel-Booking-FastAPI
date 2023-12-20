from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.bookings.repository import BookingRepository
from app.bookings.schemas import SchemaBooking, SchemaUserBooking
from app.bookings.service import get_user_bookings, try_remove_booking
from app.exceptions import RoomCantBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("/")
async def get_bookings(
        user: Annotated[User, Depends(get_current_user)]
) -> list[SchemaUserBooking]:
    return await get_user_bookings(user)


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Annotated[User, Depends(get_current_user)]
) -> SchemaBooking:
    booking = await BookingRepository.add(user.id, room_id, date_from, date_to)

    if not booking:
        raise RoomCantBeBooked

    booking_dict = SchemaBooking.model_validate(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)

    return booking


@router.delete("/{booking_id}")
async def delete_booking(
        booking_id: int,
        response: Response,
        user: Annotated[User, Depends(get_current_user)]
) -> None:
    await try_remove_booking(booking_id, user)
    response.status_code = status.HTTP_204_NO_CONTENT
