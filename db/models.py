from typing import List

from sqlalchemy import Column, Boolean, String, Table, LargeBinary
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid


Base = declarative_base()


mashup_source_link_table = Table('mashup_association', Base.metadata,
    Column('source_id', UUID(as_uuid=True), ForeignKey('sources.source_id')),
    Column('mashup_id', UUID(as_uuid=True), ForeignKey('mashups.mashup_id'))
)

author_source_link_table = Table('author_association', Base.metadata,
    Column('source_id', UUID(as_uuid=True), ForeignKey('sources.source_id')),
    Column('author_id', UUID(as_uuid=True), ForeignKey('authors.author_id'))
)

mashup_source_audio_link_table = Table('audio_association', Base.metadata,
    Column('source_id', UUID(as_uuid=True), ForeignKey('sources.source_id')),
    Column('audio_id', UUID(as_uuid=True), ForeignKey('audio.audio_id'))
)



class User(Base):
    __tablename__ = 'users'

    user_id:         Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:            Mapped[str] = Column(String, nullable=False)
    username:        Mapped[str] = Column(String, nullable=False, unique=True)
    email:           Mapped[str] = Column(String, nullable=False, unique=True)
    is_active:       Mapped[bool] = Column(Boolean(), default=True)
    hashed_password: Mapped[str] = Column(String, nullable=False)

    mashups:         Mapped[List["Mashup"]] = relationship(back_populates="user")


class Audio(Base):
    __tablename__ = 'audio'

    audio_id: Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audio:    Mapped[bytes] = Column(LargeBinary, nullable=False)

    mashups:  Mapped[List["Mashup"]] = relationship(back_populates="audio")


class Mashup(Base):
    __tablename__ = 'mashups'
    
    mashup_id:  Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:       Mapped[str] = Column(String, nullable=False)
    is_active:  Mapped[bool] = Column(Boolean(), default=True)

    audio_id:   Mapped[UUID] = mapped_column(ForeignKey('audio.audio_id'))
    user_id:    Mapped[UUID] = mapped_column(ForeignKey('users.user_id'))
    sources:    Mapped[List['Source']] = relationship(secondary=mashup_source_link_table, 
                                                      back_populates="mashup")


class Source(Base):
    __tablename__ = 'sources'

    source_id:  Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:       Mapped[str] = Column(String, nullable=False)
    is_active:  Mapped[bool] = Column(Boolean(), default=True)

    mashups:    Mapped[List[Mashup]] = relationship(secondary=mashup_source_link_table, 
                                                      back_populates="source")
    authors:    Mapped[List['Author']] = relationship(secondary=author_source_link_table, 
                                                      back_populates="source")


class Author(Base):
    __tablename__ = 'authors'

    author_id: Mapped[UUID] = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name:      Mapped[str] = Column(String, nullable=False)
    is_active: Mapped[bool] = Column(Boolean(), default=True)

    sources:   Mapped[List[Source]] = relationship(secondary=mashup_source_link_table, 
                                                      back_populates="author")
    
