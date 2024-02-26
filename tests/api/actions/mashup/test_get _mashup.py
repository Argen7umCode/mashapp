from itertools import batched, permutations
from pprint import pprint
import random
import string
from typing import Any, List
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.mashup import _get_mashups
from api.schemas.mashup import GetMashupRequest
from api.schemas.relationships import ShowMashupWithRel
from tests.db_funcs import (
    create_test_author,
    create_test_mashup,
    create_test_source,
    create_test_user,
    create_test_user_author_and_source
)
from db.models import Author, Source, User, Mashup


test_data = list(permutations(('name', 'id', 'user_id', 'source_id')))

@pytest.mark.parametrize("test_by", (test_data,))
@pytest.mark.asyncio
async def test_get_mashup(test_by: str,
    _get_test_db: AsyncSession,
    prepare_valid_test_user_data: dict[str, str],
    prepare_valid_test_mashup_data: dict[str, str],
    prepare_valid_test_source_data: dict[str, str],
    prepare_valid_test_author_data: dict[str, str],
) -> None:
    async with _get_test_db as session:
        user, author, source = await create_test_user_author_and_source(
            prepare_valid_test_user_data,
            prepare_valid_test_author_data,
            prepare_valid_test_source_data,
            session
        )
        mashup_data = prepare_valid_test_mashup_data | {
            "user_id": user.id,
            'user': user,
            "sources": [source],
        }

        inserted_mashup = await create_test_mashup(mashup_data, session)

        test = {}
        if test_by == 'id':
            test["id"] = inserted_mashup.id
        if test_by == 'name':
            test["name"] = inserted_mashup.name
        if test_by == 'user_id':
            test["user_id"] = inserted_mashup.user_id
        if test_by == 'source_id':
            test["source_id"] = inserted_mashup.sources[0].id
        
            
        request = GetMashupRequest(
            **test
        )

        getted_mashups = await _get_mashups(request, session)
        getted_mashup = getted_mashups[0]

        assert isinstance(getted_mashups, list)
        assert len(getted_mashups) == 1
        assert isinstance(getted_mashup, ShowMashupWithRel)
        assert getted_mashup.id == inserted_mashup.id
        assert getted_mashup.name == inserted_mashup.name
        assert getted_mashup.audio == inserted_mashup.audio
        assert dict(getted_mashup.user) == dict(inserted_mashup.user.to_schema_without_rel())
        assert len(getted_mashup.sources) == 1
        assert dict(getted_mashup.sources[0]) == dict(inserted_mashup.sources[0].to_schema_without_rel())


def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))



users = [
    {
        "id": None,
        "name": generate_random_string(),
        "username": generate_random_string(),
        "email": generate_random_string() + "@mail.com",
        "hashed_password": generate_random_string(),
        "is_active": True,
    } for _ in range(10)
]
mashups = [
    {
        "id": None,
        "name": generate_random_string(),
        "is_active": True,
        "audio": bytes(1),
    } for _ in range(30)
]
sources = [
    {
        "id": None,
        "name": generate_random_string(),
        "is_active": True,
        "audio": bytes(1),
    } for _ in range(30)
]
authors = [
    {
        "id": None, 
        "name": generate_random_string(), 
        "is_active": True
    } for _ in range(10)
]


async def setup_db(users: List[dict], mashups: List[dict], sources: List[dict], authors: List[dict], session: AsyncSession) -> tuple[List[User], 
                                                                                                                                     List[Mashup],
                                                                                                                                     List[Source],
                                                                                                                                     List[Author]]:
    inserted_users = []
    inserted_mashups = []
    inserted_sources = []
    inserted_authors = []

    for user_data, source_batch, author_data, mashups_batch in zip(users, 
                                                                    batched(sources, 3), 
                                                                    authors, 
                                                                    batched(mashups, 3)):
        user = await create_test_user(user_data, session)
        author = await create_test_author(author_data, session)

        inserted_users.append(user)
        inserted_authors.append(author)
        for source_data in source_batch:
            source_data = source_data | {
                "author_id": author.id,
                "author": author,
            }
            source = await create_test_source(source_data, session)
            inserted_sources.append(source)

        for mushup_data in mashups_batch:
            mashup_data = mushup_data | {
                "user_id": user.id,
                'user': user,
                "sources": [source],
            }
            inserted_mashup = await create_test_mashup(mashup_data, session)
            inserted_mashups.append(inserted_mashup)
    return (inserted_users, inserted_mashups, inserted_sources, inserted_authors)


@pytest.mark.parametrize('users_data, mashups_data, sources_data, authors_data', ((users,  mashups, sources, authors),))
@pytest.mark.asyncio
async def test_get_many_mashup_by_user_id(
    _get_test_db: AsyncSession,
    users_data: dict,
    mashups_data: dict,
    sources_data: dict,
    authors_data: dict
) -> None:
    async with _get_test_db as session:
        db = await setup_db(users_data, mashups_data, sources_data, authors_data, session)
        users: List[User] = db[0]
        mashups: List[Mashup] = db[1]
        sources: List[Source] = db[2]
        authors: List[Author] = db[3]
        for i, user in enumerate(users):
            print(i)
            request = GetMashupRequest(
                user_id=user.id
            )
            getted_mashups: List[ShowMashupWithRel] = await _get_mashups(request, session)

            assert len(getted_mashups) == len(user.mashups)
            for getted_mashup, db_mashup in zip(getted_mashups, mashups[i*3:(i+1)*3]):

                assert getted_mashup.id == db_mashup.id
                assert getted_mashup.name == db_mashup.name
                assert dict(getted_mashup.user) == dict(db_mashup.user.to_schema_without_rel())
                
                for source, db_source in zip(getted_mashup.sources, db_mashup.sources):
                    assert dict(source) == dict(db_source.to_schema_without_rel())


            

