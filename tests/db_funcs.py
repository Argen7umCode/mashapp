from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Author, Base, User, Mashup, Source


async def insert_into_db(data: Base, session: AsyncSession) -> None:
    session.add(data)
    await session.flush()


async def create_test_user(user_data: dict[str, str], session: AsyncSession) -> User:
    user = User(**user_data)
    await insert_into_db(user, session)
    return user


async def create_test_mashup(
    mashup_data: dict[str, str], session: AsyncSession
) -> Mashup:
    mashup = Mashup(**mashup_data)
    await insert_into_db(mashup, session)
    return mashup


async def create_test_source(
    source_data: dict[str, str], session: AsyncSession
) -> Source:
    source = Source(**source_data)
    await insert_into_db(source, session)
    return source


async def create_test_author(
    author_data: dict[str, str], session: AsyncSession
) -> Source:
    author = Author(**author_data)
    await insert_into_db(author, session)
    return author
