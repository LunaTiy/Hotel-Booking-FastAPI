from typing import Optional, List

from sqlalchemy import Integer, ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    services: Mapped[Optional[List[str]]] = mapped_column(JSON)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    image_id: Mapped[Optional[int]] = mapped_column(Integer)
