from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class SchemaBooking(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int


class SchemaUserBooking(BaseModel):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    image_id: Optional[int]
    name: str
    description: Optional[str]
    services: Optional[List[str]]
