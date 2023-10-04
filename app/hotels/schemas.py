
from pydantic import BaseModel


class SchemaHotel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str] | None
    rooms_quantity: int
    image_id: int | None


class SchemaAvailableHotel(SchemaHotel):
    rooms_left: int
