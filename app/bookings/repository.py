﻿from datetime import date

from sqlalchemy import func, insert, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Booking
from app.database import async_session_maker
from app.hotels.rooms.models import Room
from app.logger import logger
from app.repository.base import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    model = Booking

    @classmethod
    async def get_count_available_rooms(
            cls,
            room_id: int,
            date_from: date,
            date_to: date
    ) -> int:
        booked_rooms = (
            select(cls.model)
            .where(
                (Booking.room_id == room_id)
                & ((Booking.date_from <= date_to) & (Booking.date_to >= date_from))
            )
            .cte("booked_rooms")
        )

        get_rooms_left = (
            select(
                (Room.quantity - func.count(booked_rooms.columns.room_id)).label(
                    "rooms_left"
                )
            )
            .select_from(Room)
            .join(booked_rooms, booked_rooms.columns.room_id == Room.id, isouter=True)
            .where(Room.id == room_id)
            .group_by(Room.quantity, booked_rooms.columns.room_id)
        )

        async with async_session_maker() as session:
            rooms_left_result = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left_result.mappings().one().rooms_left
            return rooms_left

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date
    ) -> model | None:
        """
        -- Заезд '2023-05-15'
        -- Выезд '2023-06-20'
        -- Комната с ид 1

        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            (date_from <= '2023-06-20' AND date_to >= '2023-05-15')
        )

        SELECT rooms.quantity - count(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id
        """
        try:
            rooms_left = await cls.get_count_available_rooms(room_id, date_from, date_to)
            if rooms_left <= 0:
                return None

            async with async_session_maker() as session:
                get_price = select(Room.price).filter(Room.id == room_id)
                price = await session.execute(get_price)

                current_price: int = price.mappings().one().price

                add_booking = (
                    insert(cls.model)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=current_price,
                    )
                    .returning(Booking.__table__.columns)
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.mappings().one()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exception: Can't add booking"
            else:
                msg = "Unknown Exception: Can't add booking"

            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from": date_from,
                "date_to": date_to,
            }

            logger.error(msg, extra=extra, exc_info=True)
