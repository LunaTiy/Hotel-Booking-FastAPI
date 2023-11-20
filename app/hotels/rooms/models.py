from typing import TYPE_CHECKING

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.bookings.models import Booking
    from app.hotels.models import Hotel


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    services: Mapped[list[str] | None] = mapped_column(JSON)
    quantity: Mapped[int]
    image_id: Mapped[int | None]

    hotel: Mapped["Hotel"] = relationship("Hotel", back_populates="rooms")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="room")

    def __str__(self) -> str:
        return f"Номер #{self.id}, {self.name}"
