from datetime import date
from typing import Optional, List

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel

app = FastAPI()


class HotelSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            has_spa: Optional[bool] = None,
            stars: Optional[int] = Query(None, ge=1, le=5)
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


class SchemaHotel(BaseModel):
    address: str
    name: str
    stars: int


@app.get("/hotels")
def get_hotels(
        search_args: HotelSearchArgs = Depends()
) -> List[SchemaHotel]:
    hotels = [
        SchemaHotel(address="New-York city, green street, house 5", name="Great hotel", stars=4)
    ]
    return hotels


class SchemaBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def add_booking(booking: SchemaBooking):
    pass
