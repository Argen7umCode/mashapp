from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Base


async def insert_into_db(data: Base, session: AsyncSession) -> None:
    session.add(data)
    await session.flush()
