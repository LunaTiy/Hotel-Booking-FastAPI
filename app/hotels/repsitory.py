from app.hotels.models import Hotel
from app.repository.base import BaseRepository


class HotelRepository(BaseRepository):
    model = Hotel
