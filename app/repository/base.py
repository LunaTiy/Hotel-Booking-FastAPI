from typing import Any, Generic, TypeVar

from sqlalchemy import delete, insert, select, update

from app.database import async_session_maker

T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: T = None

    @classmethod
    async def add(cls, **data: str) -> None:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def remove(cls, *filter_by: list[bool]) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).filter(*filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, *filter_by: list[bool], **data: dict[str, Any]) -> list[T]:
        async with async_session_maker() as session:
            query = update(cls.model).filter(*filter_by).values(**data).returning(
                cls.model.__table__.columns)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().all()

    @classmethod
    async def find_one_or_none(cls, *filter_by: list[bool]) -> T | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(*filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, *filter_by: list[bool]) -> list[T]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(*filter_by)
            result = await session.execute(query)
            return result.mappings().all()
