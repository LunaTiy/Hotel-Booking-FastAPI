from datetime import date
from typing import List

from fastapi import APIRouter

from app.hotels.rooms.schemas import SchemaRoom
from app.hotels.rooms.service import get_rooms_by_schema
from app.hotels.router import router as hotels_router

router = APIRouter(
    prefix=f"{hotels_router.prefix}",
    tags=["Отели"]
)


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date) -> List[SchemaRoom]:
    return await get_rooms_by_schema(date_from, date_to, hotel_id)
