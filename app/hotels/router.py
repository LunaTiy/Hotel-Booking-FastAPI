import asyncio
from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.hotels.models import Hotel
from app.hotels.repsitory import HotelRepository
from app.hotels.schemas import SchemaAvailableHotel, SchemaHotel
from app.hotels.service import get_available_hotels

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/{location}")
@cache(expire=20)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: date = Query(description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(description=f"Например, {datetime.now().date()}")
) -> List[SchemaAvailableHotel]:
    hotels = await get_available_hotels(location, date_from, date_to)
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> Optional[SchemaHotel]:
    return await HotelRepository.find_one_or_none(Hotel.id == hotel_id)
