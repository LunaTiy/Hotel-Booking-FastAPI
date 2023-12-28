from datetime import date, datetime
from typing import Annotated

from fastapi import APIRouter, Query

from app.exceptions import IncorrectDataFormat, IncorrectDataFormatDiapason
from app.hotels.models import Hotel
from app.hotels.repsitory import HotelRepository
from app.hotels.schemas import SchemaAvailableHotel, SchemaHotel
from app.hotels.service import get_available_hotels

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/{location}")
# @cache(expire=20)
async def get_hotels_by_location_and_time(
        location: str,
        date_from: Annotated[date, Query(description=f"Например, {datetime.now().date()}")],
        date_to: Annotated[date, Query(description=f"Например, {datetime.now().date()}")]
) -> list[SchemaAvailableHotel]:
    if date_from > date_to:
        raise IncorrectDataFormat

    if (date_to - date_from).days > 30:
        raise IncorrectDataFormatDiapason

    return await get_available_hotels(location, date_from, date_to)


@router.get("/id/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> SchemaHotel | None:
    return await HotelRepository.find_one_or_none(Hotel.id == hotel_id)
