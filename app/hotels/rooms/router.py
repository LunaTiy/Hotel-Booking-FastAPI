from datetime import date, datetime
from typing import List

from fastapi import APIRouter, Query

from app.hotels.rooms.schemas import SchemaRoom
from app.hotels.rooms.service import get_rooms_with_cost_and_left
from app.hotels.router import router as hotels_router

router = APIRouter(
    prefix=f"{hotels_router.prefix}",
    tags=["Отели"]
)


@router.get("/{hotel_id}/rooms")
async def get_rooms_by_time(
        hotel_id: int,
        date_from: date = Query(description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(description=f"Например, {datetime.now().date()}")
) -> List[SchemaRoom]:
    return await get_rooms_with_cost_and_left(date_from, date_to, hotel_id)
