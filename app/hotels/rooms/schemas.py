
from pydantic import BaseModel


class SchemaRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str | None
    price: int
    services: list[str] | None
    quantity: int
    image_id: int | None
    total_cost: int
    rooms_left: int
