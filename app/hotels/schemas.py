from typing import Optional, List

from pydantic import BaseModel


class SchemaHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[List[str]]
    rooms_quantity: int
    image_id: Optional[int]


class SchemaAvailableHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[List[str]]
    rooms_quantity: int
    image_id: Optional[int]
    rooms_left: int
