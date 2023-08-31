from datetime import date
from typing import List

from fastapi import APIRouter

from app.hotels.schemas import SchemaAvailableHotel
from app.hotels.service import get_available_hotels

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("/{location}")
async def get_hotels(location: str, date_from: date, date_to: date) -> List[SchemaAvailableHotel]:
    return await get_available_hotels(location, date_from, date_to)
