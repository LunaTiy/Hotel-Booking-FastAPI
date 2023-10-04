from datetime import date

from app.bookings.repository import BookingRepository
from app.hotels.models import Hotel
from app.hotels.repsitory import HotelRepository
from app.hotels.rooms.models import Room
from app.hotels.rooms.repository import RoomRepository
from app.hotels.schemas import SchemaAvailableHotel


async def get_available_hotels(location: str, date_from: date, date_to: date) -> list[SchemaAvailableHotel]:
    hotels: list[Hotel] = await HotelRepository.find_all(Hotel.location.contains(location))
    available_hotels: list[SchemaAvailableHotel] = []

    for hotel in hotels:
        rooms: list[Room] = await RoomRepository.find_all(Room.hotel_id == hotel.id)
        common_rooms_left = 0

        for room in rooms:
            rooms_left = await BookingRepository.get_count_available_rooms(room.id, date_from, date_to)
            common_rooms_left += rooms_left

        if common_rooms_left < 1:
            continue

        available_hotel = SchemaAvailableHotel(
            id=hotel.id,
            name=hotel.name,
            location=hotel.location,
            services=hotel.services,
            rooms_quantity=hotel.rooms_quantity,
            image_id=hotel.image_id,
            rooms_left=common_rooms_left
        )
        available_hotels.append(available_hotel)

    return available_hotels
