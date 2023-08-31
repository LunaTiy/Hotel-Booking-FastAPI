from typing import List

from app.bookings.repository import BookingRepository
from app.hotels.rooms.models import Room
from app.hotels.rooms.repository import RoomRepository
from app.hotels.rooms.schemas import SchemaRoom


async def get_rooms_by_schema(date_from, date_to, hotel_id):
    rooms: List[Room] = await RoomRepository.find_all(Room.hotel_id == hotel_id)
    output_rooms: List[SchemaRoom] = []

    for room in rooms:
        rooms_left = await BookingRepository.get_count_available_rooms(room.id, date_from, date_to)
        total_cost = room.price * (date_to - date_from).days

        output_rooms.append(
            SchemaRoom(
                id=room.id,
                hotel_id=room.hotel_id,
                name=room.name,
                description=room.description,
                price=room.price,
                services=room.services,
                quantity=room.quantity,
                image_id=room.image_id,
                total_cost=total_cost,
                rooms_left=rooms_left,
            )
        )

    return output_rooms
