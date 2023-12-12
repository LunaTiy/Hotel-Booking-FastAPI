import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession  # noqa

from app.bookings.models import Booking
from app.config import settings
from app.database import Base, async_session_maker, engine
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.main import app as fastapi_app
from app.users.models import User


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database() -> None:
    assert settings.mode == "TEST"

    async with engine.begin() as conn:  # type: AsyncConnection
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    bookings, hotels, rooms, users = await read_and_process_data()

    async with async_session_maker() as session:
        await insert_test_data(session, Hotel, hotels)
        await insert_test_data(session, Room, rooms)
        await insert_test_data(session, User, users)
        await insert_test_data(session, Booking, bookings)

        await session.commit()


# @pytest.fixture(scope="session")
# def event_loop():
#     """
#     Create an instance of the default event loop for each test case
#     TODO: may be remove
#     """
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def async_db_session():
    """todo: возможно не пригодится"""
    async with async_session_maker() as session:
        yield session


def open_mock_json(model: str) -> list[dict[str, Any]] | dict[str, Any]:
    file_path = Path(f"app/tests/mocks/mock_{model}.json")
    with file_path.open(encoding="utf-8") as file:
        return json.load(file)


async def read_and_process_data() -> tuple[list[Any], list[Any], list[Any], list[Any]]:
    hotels = open_mock_json("hotels")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")
    bookings = open_mock_json("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    return bookings, hotels, rooms, users


async def insert_test_data(
        session: AsyncSession,
        table: type[Base],
        values: list[dict[str, Any]]
) -> None:
    insert_data = insert(table).values(values)
    await session.execute(insert_data)
