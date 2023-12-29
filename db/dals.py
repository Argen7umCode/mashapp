from typing import Any, List, Union


from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Base
from db.models import User, Mashup, Source, Audio, Author
from db.models import mashup_source_link_table, author_source_link_table


class DAL:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def _create(self, new_item) -> Base:
        self.db_session.add(new_item)
        await self.db_session.flush()
        return new_item

    async def _make_query_and_get_all(self, query) -> Union[User, None]:
        res = await self.db_session.execute(query)
        row = res.fetchall()
        if row is not None:
            return row

    async def _make_query_and_get_one(self, query) -> Union[User, None]:
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is not None:
            return row

    async def _get_all_by_field_value(self, table: Base, field, value: Any):
        query = select(table).where(field == value)
        return await self._make_query_and_get_all(query)

    async def _get_one_by_field_value(self, table: Base, field, value):
        query = select(table).where(field == value)
        return await self._make_query_and_get_all(query)

    async def _get_by_id(self, id: int, table):
        return await self._get_one_by_field_value(table, table.user_id, id)

    async def is_exists(self, id: int) -> bool:
        item = await self.get_by_id(id)
        return item if item is not None else False


class UserDAL(DAL):
    async def create_user(
        self,
        name: str,
        username: str,
        email: str,
        is_active: bool,
        hashed_password: str,
        mashups: list,
    ) -> User:
        new_user = User(
            name=name,
            username=username,
            email=email,
            is_active=is_active,
            hashed_password=hashed_password,
        )
        return await self._create(new_user)

    async def get_by_id(self, user_id: int) -> Union[User, None]:
        return await self._get_by_id(user_id, User)

    async def get_user_by_mashup_id(self, mashup_id: int) -> Union[User, None]:
        query = select(User).join(Mashup).where(Mashup.mashup_id == mashup_id)
        return await self._make_query_and_get_one(query)

    async def get_user_by_email(self, email: str) -> Union[User, None]:
        return await self._get_one_by_field_value(User, User.email, email)

    async def delete_user(self, user_id: int) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.user_id)
        )
        return await self._make_query_and_get_one(query)

    async def update_user(self, user_id, **kwargs) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.user_id)
        )
        return await self._make_query_and_get_one(query)


class MashupDAL(DAL):
    async def create_mashup(
        self, name: str, audio_id: bytes, user_id: int, sources: list
    ) -> Mashup:
        new_mashup = Mashup(
            name=name,
            audio_id=audio_id,
            user_id=user_id,
            is_active=True,
            sources=sources,
        )
        return await self._create(new_mashup)

    async def get_by_id(self, mashup_id: int) -> Mashup:
        return await self._get_by_id(mashup_id, Mashup)

    async def get_mashups_by_name(self, name: str) -> Mashup:
        return await self._get_one_by_field_value(Mashup, Mashup.name, name)

    async def get_mashups_by_user_id(self, user_id: int) -> List[Mashup]:
        query = select(Mashup).where(Mashup.user_id == user_id)
        return await self._make_query_and_get_all(query)

    async def get_mashups_by_source_id(self, source_id: int) -> List[Mashup]:
        query = (
            select(Mashup)
            .join(mashup_source_link_table)
            .filter(mashup_source_link_table.c.source_id == source_id)
        )
        return await self._make_query_and_get_all(query)

    async def get_author_by_audio_id(self, audio_id: int) -> Mashup:
        query = select(Mashup).join(Audio).filter(Audio.audio_id == audio_id)
        return await self._make_query_and_get_all(query)

    async def delete_mashup(self, mashup_id: int) -> Union[int, None]:
        query = (
            update(Mashup)
            .where(and_(Mashup.mashup_id == mashup_id, Mashup.is_active == True))
            .values(is_active=False)
            .returning(Mashup.mashup_id)
        )
        return await self._make_query_and_get_one(query)

    async def update_mashup(self, mashup_id, **kwargs) -> Union[int, None]:
        query = (
            update(Mashup)
            .where(and_(Mashup.mashup_id == mashup_id, Mashup.is_active == True))
            .values(kwargs)
            .returning(Mashup.mashup_id)
        )
        return await self._make_query_and_get_one(query)


class SourceDAL(DAL):
    async def create_source(
        self, name: str, is_active: bool, mashups: list, authors: list
    ) -> Source:
        new_source = Source(
            name=name, is_active=is_active, mashups=mashups, authors=authors
        )
        return await self._create(new_source)

    async def get_by_id(self, source_id: int) -> Source:
        return await self._get_by_id(source_id, Source)

    async def get_sources_by_mashup_id(self, mashup_id: int) -> Source:
        query = (
            select(Source)
            .join(mashup_source_link_table)
            .filter(mashup_source_link_table.c.mashup_id == mashup_id)
        )
        return await self._make_query_and_get_all(query)

    async def get_sources_by_author_id(self, author_id: int) -> Source:
        query = (
            select(Source)
            .join(author_source_link_table)
            .filter(author_source_link_table.c.author_id == author_id)
        )
        return await self._make_query_and_get_all(query)

    async def get_sources_by_name(self, name: str) -> Source:
        return await self._get_one_by_field_value(Source, Source.name, name)

    async def delete_source(self, source_id: int) -> Union[int, None]:
        query = (
            update(Source)
            .where(and_(Source.source_id == source_id, Source.is_active == True))
            .values(is_active=False)
            .returning(Source.source_id)
        )
        return await self._make_query_and_get_one(query)

    async def update_source(self, source_id, **kwargs) -> Union[int, None]:
        query = (
            update(Source)
            .where(and_(Source.source_id == source_id, Source.is_active == True))
            .values(kwargs)
            .returning(Source.source_id)
        )
        return await self._make_query_and_get_one(query)


class AuthorDAL(DAL):
    async def create_author(self, name: str, is_active: bool, sources: list) -> Author:
        new_author = Author(name=name, is_active=is_active, sources=sources)
        self._create(new_author)

    async def get_by_id(self, author_id: int) -> Author:
        return await self._get_by_id(author_id, Author)

    async def get_author_by_source_id(self, source_id: int) -> Author:
        query = (
            select(Author)
            .join(author_source_link_table)
            .filter(author_source_link_table.c.source_id == source_id)
        )
        return await self._make_query_and_get_all(query)

    async def delete_author(self, author_id: int) -> Union[int, None]:
        query = (
            update(Author)
            .where(and_(Author.author_id == author_id, Author.is_active == True))
            .values(is_active=False)
            .returning(Author.author_id)
        )
        return await self._make_query_and_get_one(query)

    async def update_author(self, author_id: int, **kwargs) -> Union[int, None]:
        query = (
            update(Author)
            .where(and_(Author.author_id == author_id, Author.is_active == True))
            .values(kwargs)
            .returning(Author.author_id)
        )
        return await self._make_query_and_get_one(query)


class AudioDAL(DAL):
    async def create_audio(self, audio: bytes) -> Audio:
        new_audio = Audio(audio=audio, mashups=[])
        return await self._create(new_audio)

    async def get_by_id(self, audio_id: int) -> Audio:
        return await self._get_by_id(audio_id, Audio)

    async def get_audio_by_mashup_id(self, mashup_id: int) -> Audio:
        query = select(Audio).join(Mashup).filter(Mashup.mashup_id == mashup_id)
        return await self._make_query_and_get_one(query)

    async def delete_audio(self, audio_id: int) -> Union[int, None]:
        query = (
            update(Audio)
            .where(and_(Audio.audio_id == audio_id, Audio.is_active == True))
            .values(is_active=False)
            .returning(Audio.audio_id)
        )
        return await self._make_query_and_get_one(query)

    async def update_audio(self, audio_id: int, **kwargs) -> Union[int, None]:
        query = (
            update(Audio)
            .where(and_(Audio.audio_id == Audio, Audio.is_active == True))
            .values(kwargs)
            .returning(Audio.audio_id)
        )
        return await self._make_query_and_get_one(query)
