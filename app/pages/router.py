﻿from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
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
        hotels: Annotated[list[SchemaAvailableHotel], Depends(get_hotels_by_location_and_time)]
) -> Response:
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels}
    )
