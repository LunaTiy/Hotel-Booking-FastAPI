from typing import Optional

from sqlalchemy import Integer, String, JSON, SmallInteger
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    services: Mapped[Optional[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    image_id: Mapped[int] = mapped_column(Integer)
