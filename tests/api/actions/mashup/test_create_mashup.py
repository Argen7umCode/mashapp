import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from api.actions.mashup import _create_mashup
from api.schemas.mashup import CreateMashupRequest, ShowMashup
from api.schemas.relationships import ShowMashupWithRel
from tests.db_funcs import (
    insert_into_db,
    create_test_source,
    create_test_user,
    create_test_author,
)
from db.models import Author, Source, User, Mashup


async def create_test_user_author_and_source(
    user_data: dict[str, str],
    author_data: dict[str, str],
    source_data: dict[str, str],
    session: AsyncSession,
) -> tuple[User, Author, Source]:
    user = await create_test_user(user_data, session)
    author = await create_test_author(author_data, session)

    source_data = source_data | {
        "author_id": author.id,
        "author": author,
    }
    source = await create_test_source(source_data, session)
    return user, author, source

@pytest.mark.asyncio
async def test_sucssess_creating_mashup(
    _get_test_db: AsyncSession,
    prepare_valid_test_user_data: dict[str, str],
    prepare_valid_test_mashup_data: dict[str, str],
    prepare_valid_test_source_data: dict[str, str],
    prepare_valid_test_author_data: dict[str, str],
) -> None:
    async with _get_test_db as session:
        user, author, source = await create_test_user_author_and_source(prepare_valid_test_user_data, 
                                                                        prepare_valid_test_author_data,
                                                                        prepare_valid_test_source_data,
                                                                        session)

        mashup_data = prepare_valid_test_mashup_data | {
            "user_id": user.id,
            "sources_ids": [source.id],
        }
        request = CreateMashupRequest(**mashup_data)

        mashup = await _create_mashup(request, session)
        
        query = select(Mashup).where(Mashup.id == mashup.id)
        response = (await session.execute(query)).scalar_one_or_none()

        assert isinstance(mashup, ShowMashupWithRel)
        assert mashup.id == response.id
        assert mashup.name == response.name
        assert mashup.is_active == response.is_active
        assert mashup.audio == response.audio
        assert len(mashup.sources) == len(response.sources)
        assert dict(mashup.user) == dict(response.user.to_schema_without_rel())
        for source, res_source in zip(mashup.sources, response.sources):
            assert dict(source) == dict(res_source.to_schema_without_rel())
        