from datetime import date
from typing import Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


@app.get("/hotels")
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        has_spa: Optional[bool] = None,
        stars: Optional[int] = Query(None, ge=1, le=5)
):
    return location, date_from, date_to, has_spa, stars


class SchemaBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def add_booking(booking: SchemaBooking):
    pass
