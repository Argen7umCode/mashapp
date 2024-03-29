from abc import ABC, abstractmethod
from typing import List, Annotated, Optional, Union

from sqlalchemy import Column, LargeBinary, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, MappedAsDataclass
from sqlalchemy.orm import DeclarativeBase

from api.schemas.user import ShowUser
from api.schemas.mashup import ShowMashup
from api.schemas.source import ShowSource
from api.schemas.author import ShowAuthor
from api.schemas.relationships import (
    ShowUserWithRel,
    ShowMashupWithRel,
    ShowSourceWithRel,
    ShowAuthorWithRel,
)
from api.schemas import BaseModel


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


primary_key_int = Annotated[int, mapped_column(primary_key=True)]
unique_nonnull_str = Annotated[str, mapped_column(nullable=False, unique=True)]
nonnull_str = Annotated[str, mapped_column(nullable=False)]
is_active = Annotated[bool, mapped_column(default=True)]
audio = Annotated[bytes, mapped_column(LargeBinary, nullable=False)]


MashupSourceLink = Table(
    "mashup_source_table",
    Base.metadata,
    Column("mashup_id", ForeignKey("mashups.id"), primary_key=True),
    Column("source_id", ForeignKey("sources.id"), primary_key=True),
)


class SchemaMixin:
    def to_schema(self, schema: BaseModel) -> BaseModel:
        return schema.model_validate(self, from_attributes=True)


class User(MappedAsDataclass, Base, SchemaMixin):
    __tablename__ = "users"

    id: Mapped[primary_key_int]
    name: Mapped[nonnull_str]
    username: Mapped[unique_nonnull_str]
    email: Mapped[unique_nonnull_str]
    is_active: Mapped[is_active]
    hashed_password: Mapped[nonnull_str]

    mashups: Mapped[Optional[List["Mashup"]]] = relationship(
        default_factory=lambda: [], back_populates="user", lazy="subquery"
    )

    def to_schema_without_rel(self) -> ShowUser:
        return self.to_schema(ShowUser)

    def to_schema_with_rel(self) -> ShowUserWithRel:
        return self.to_schema(ShowUserWithRel)


class Mashup(MappedAsDataclass, Base, SchemaMixin):
    __tablename__ = "mashups"

    id: Mapped[primary_key_int]
    name: Mapped[nonnull_str]
    is_active: Mapped[is_active]
    audio: Mapped[audio]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="mashups")
    sources: Mapped[List["Source"]] = relationship(
        back_populates="mashups",
        secondary="mashup_source_table",
        default_factory=lambda: [],
        lazy="subquery",
    )

    def to_schema_without_rel(self) -> ShowUser:
        return self.to_schema(ShowMashup)

    def to_schema_with_rel(self) -> ShowMashupWithRel:
        return self.to_schema(ShowMashupWithRel)


class Source(MappedAsDataclass, Base, SchemaMixin):
    __tablename__ = "sources"

    id: Mapped[primary_key_int]
    name: Mapped[nonnull_str]
    audio: Mapped[audio]
    is_active: Mapped[is_active]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    author: Mapped["Author"] = relationship(back_populates="sources")
    mashups: Mapped[List["Mashup"]] = relationship(
        back_populates="sources",
        secondary="mashup_source_table",
        default_factory=lambda: [],
        lazy="subquery",
    )

    def to_schema_without_rel(self) -> ShowSource:
        return self.to_schema(ShowSource)

    def to_schema_with_rel(self) -> ShowSourceWithRel:
        return self.to_schema(ShowSourceWithRel)


class Author(MappedAsDataclass, Base, SchemaMixin):
    __tablename__ = "authors"

    id: Mapped[primary_key_int]
    name: Mapped[nonnull_str]
    is_active: Mapped[is_active]
    sources: Mapped[List["Source"]] = relationship(
        back_populates="author", default_factory=lambda: [], lazy="subquery"
    )

    def to_schema_without_rel(self) -> ShowAuthor:
        return self.to_schema(ShowAuthor)

    def to_schema_with_rel(self) -> ShowAuthorWithRel:
        return self.to_schema(ShowAuthorWithRel)
