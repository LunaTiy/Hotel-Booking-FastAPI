from typing import Optional, List

from pydantic import BaseModel


class SchemaHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[List[str]]
    rooms_quantity: int
    image_id: Optional[int]


class SchemaAvailableHotel(SchemaHotel):
    rooms_left: int
