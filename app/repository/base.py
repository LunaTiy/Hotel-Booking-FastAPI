from sqlalchemy import select, insert, update, delete

from app.database import async_session_maker


class BaseRepository:
    model = None

    @classmethod
    async def add(cls, **data) -> None:
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def remove(cls, *filter_by) -> None:
        async with async_session_maker() as session:
            query = delete(cls.model).filter(*filter_by)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, *filter_by, **data):
        async with async_session_maker() as session:
            query = update(cls.model.__table__.columns).filter(*filter_by).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().all()

    @classmethod
    async def find_one_or_none(cls, *filter_by) -> model | None:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(*filter_by)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, *filter_by) -> list[model]:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter(*filter_by)
            result = await session.execute(query)
            return result.mappings().all()
