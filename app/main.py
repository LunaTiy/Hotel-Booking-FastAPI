from datetime import date
from typing import Optional, List

from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel

from app.bookings.router import router as bookings_router
from app.hotels.router import router as hotels_router
from app.users.router import router as users_router

app = FastAPI()
app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(bookings_router)


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
def get_hotels(search_args: HotelSearchArgs = Depends()) -> List[SchemaHotel]:
    hotels = [
        SchemaHotel(address="New-York city, green street, house 5", name="Great hotel", stars=4)
    ]
    return hotels
