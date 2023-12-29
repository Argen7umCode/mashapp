from typing import List, Annotated

from sqlalchemy import Column, LargeBinary, Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import DeclarativeBase


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


class User(Base):
    __tablename__ = "users"

    id: Mapped[primary_key_int]
    name: Mapped[nonnull_str]
    username: Mapped[unique_nonnull_str]
    email: Mapped[unique_nonnull_str]
    is_active: Mapped[is_active]
    hashed_password: Mapped[nonnull_str]

    mashups: Mapped[List["Mashup"]] = relationship(back_populates="user")


class Mashup(Base):
    __tablename__ = "mashups"

    id: Mapped[primary_key_int]
    name: Mapped[nonnull_str]
    is_active: Mapped[is_active]
    audio: Mapped[audio]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship(back_populates="mashups")
    sources: Mapped[List["Source"]] = relationship(
        back_populates="mashups", secondary="MashupSourceLink"
    )


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[primary_key_int]
    name: Mapped[nonnull_str]
    audio: Mapped[audio]
    is_active: Mapped[is_active]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    author: Mapped["Author"] = relationship(back_populates="sources")
    mashups: Mapped[List["Source"]] = relationship(
        back_populates="sources", secondary="MashupSourceLink"
    )


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[primary_key_int]
    name: Mapped[nonnull_str]
    is_active: Mapped[is_active]
    sources: Mapped[List["Source"]] = relationship(back_populates="author")
