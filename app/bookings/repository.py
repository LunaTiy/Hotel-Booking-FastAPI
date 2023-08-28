from app.bookings.models import Booking
from app.repository.base import BaseRepository


class BookingRepository(BaseRepository):
    model = Booking
