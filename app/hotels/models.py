﻿from typing import TYPE_CHECKING

from sqlalchemy import JSON, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.hotels.rooms.models import Room


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    location: Mapped[str] = mapped_column(String(255))
    services: Mapped[list[str] | None] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(SmallInteger)
    image_id: Mapped[int | None]

    rooms: Mapped[list["Room"]] = relationship("Room", back_populates="hotel")

    def __str__(self) -> str:
        return f"Отель {self.name}, {self.location[:30]}..."
