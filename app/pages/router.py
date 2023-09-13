from typing import List

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_location_and_time
from app.hotels.schemas import SchemaAvailableHotel

router = APIRouter(
    prefix="/pages",
    tags=["Фронт-энд"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_page(
        request: Request,
        hotels: List[SchemaAvailableHotel] = Depends(get_hotels_by_location_and_time)
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels}
    )
