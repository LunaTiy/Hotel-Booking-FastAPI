from datetime import date
from typing import List, Optional

from fastapi import APIRouter

from app.hotels.models import Hotel
from app.hotels.repsitory import HotelRepository
from app.hotels.schemas import SchemaAvailableHotel, SchemaHotel
from app.hotels.service import get_available_hotels

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date) -> List[SchemaAvailableHotel]:
    return await get_available_hotels(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> Optional[SchemaHotel]:
    return await HotelRepository.find_one_or_none(Hotel.id == hotel_id)
