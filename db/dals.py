import abc
from typing import Any, List, Union


from sqlalchemy import Select, and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Base
from db.models import User, Mashup, Source, Author
from db.qsm import QSMFactory
from exceptions.exceptions import UnknownFieldsException


class QSMMixin(QSMFactory):
    @classmethod
    def get_query(cls, data: dict[str, str], model: Base):
        qsm = cls.get_qsm(model)()
        return qsm.get_query(data)


class DAL(QSMMixin):
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def _create(self, new_item) -> Base:
        self.db_session.add(new_item)
        await self.db_session.flush()
        return new_item

    async def _make_query_and_get_all(self, query) -> Union[User, None]:
        res = await self.db_session.execute(query)
        rows = [row[0] for row in res.all()]
        return rows

    async def _make_query_and_get_one(self, query) -> Union[User, None]:
        res = await self.db_session.execute(query)
        row = res.scalar_one_or_none()
        return row

    async def _get_all_by_field_value(self, table: Base, field, value: Any):
        query = select(table).where(field == value)
        return await self._make_query_and_get_all(query)

    async def _get_one_by_field_value(self, table: Base, field, value):
        query = select(table).where(field == value)
        return await self._make_query_and_get_one(query)

    async def _get_by_id(self, id: int, table):
        return await self._get_one_by_field_value(table, table.id, id)

    async def is_exists(self, id: int) -> bool:
        item = await self.get_by_id(id)
        return item if item is not None else False

    async def _get(self, data: dict[str, str], model: Base) -> List[Base]:
        fields = self.get_qsm(model)().fields_to_get.keys()
        if not any(col in fields for col in data.keys()):
            raise UnknownFieldsException()
        
        query = self.get_query(data, model)
        return await self._make_query_and_get_all(query)


class UserDAL(DAL):
    async def create_user(
        self,
        name: str,
        username: str,
        email: str,
        is_active: bool,
        hashed_password: str,
    ) -> User:
        new_user = User(
            id=None,
            name=name,
            username=username,
            email=email,
            is_active=is_active,
            hashed_password=hashed_password,
        )
        return await self._create(new_user)

    async def get(self, data: dict[str, str]) -> List[User]:
        return await self._get(data, User)

    async def get_by_id(self, user_id: int) -> Union[User, None]:
        return await self._get_by_id(user_id, User)

    async def delete_user(self, user_id: int) -> Union[int, None]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.id)
        )
        return await self._make_query_and_get_one(query)

    async def update_user(self, user_id, **kwargs) -> Union[int, None]:
        if len(kwargs) == 0:
            raise ValueError("Updating user using empty data")
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.id)
        )
        return await self._make_query_and_get_one(query)


class MashupDAL(DAL):
    async def create_mashup(
        self, name: str, audio: bytes, user_id: int, user: User, sources: list
    ) -> Mashup:
        new_mashup = Mashup(
            id=None,
            name=name,
            audio=audio,
            user_id=user_id,
            user=user,
            is_active=True,
            sources=sources,
        )
        return await self._create(new_mashup)

    async def get(self, data: dict[str, str]):
        return await self._get(data, Mashup)

    async def get_by_id(self, mashup_id: int) -> Mashup:
        return await self._get_by_id(mashup_id, Mashup)
    
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

    async def get(self, data: dict[str, str]) -> List[Source]:
        return await  self._get(data, Source)

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

    async def get(self, data: dict[str, str]) -> List[Author]:
        return await  self._get(data, Author)

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
