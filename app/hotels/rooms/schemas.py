from typing import Optional, List

from pydantic import BaseModel


class SchemaRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    price: int
    services: Optional[List[str]]
    quantity: int
    image_id: int
    total_cost: int
    rooms_left: int
