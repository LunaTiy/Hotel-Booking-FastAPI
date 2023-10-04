from sqlalchemy import String, JSON, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    location: Mapped[str] = mapped_column(String(255))
    services: Mapped[list[str] | None] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(SmallInteger)
    image_id: Mapped[int | None]
