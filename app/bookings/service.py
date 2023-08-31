from typing import List

from app.bookings.models import Booking
from app.bookings.repository import BookingRepository
from app.bookings.schemas import SchemaUserBooking
from app.exceptions import CantRemoveBooking
from app.hotels.rooms.models import Room
from app.hotels.rooms.repository import RoomRepository
from app.users.models import User


async def get_user_bookings(user: User):
    bookings: List[Booking] = await BookingRepository.find_all(Booking.user_id == user.id)
    user_bookings: List[SchemaUserBooking] = []

    for booking in bookings:
        room: Room = await RoomRepository.find_one_or_none(Room.id == booking.room_id)
        user_bookings.append(
            SchemaUserBooking(
                room_id=booking.room_id,
                user_id=user.id,
                date_from=booking.date_from,
                date_to=booking.date_to,
                price=booking.price,
                total_cost=booking.total_cost,
                total_days=booking.total_days,
                image_id=room.image_id,
                name=room.name,
                description=room.description,
                services=room.services
            )
        )

    return user_bookings


async def try_remove_booking(booking_id: int, user: User):
    booking: Booking = await BookingRepository.find_one_or_none(Booking.id == booking_id, Booking.user_id == user.id)
    if not booking:
        raise CantRemoveBooking
    await BookingRepository.remove(Booking.id == booking_id)
