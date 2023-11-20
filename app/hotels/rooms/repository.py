from app.hotels.rooms.models import Room
from app.repository.base import BaseRepository


class RoomRepository(BaseRepository[Room]):
    model = Room
