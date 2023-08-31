﻿from datetime import date
from typing import List

from fastapi import APIRouter, Depends

from app.bookings.repository import BookingRepository
from app.bookings.schemas import SchemaBooking
from app.bookings.service import get_user_bookings
from app.exceptions import RoomCantBeBooked
from app.users.dependencies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def get_bookings(user: User = Depends(get_current_user)) -> List[SchemaBooking]:
    return await get_user_bookings(user)


@router.post("/add")
async def add_booking(
        room_id: int, date_from: date, date_to: date,
        user: User = Depends(get_current_user),
):
    booking = await BookingRepository.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCantBeBooked

    return booking
