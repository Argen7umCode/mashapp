
import asyncio
import pytest


from api.actions.user import (
    _create_user,
)

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from api.schemas.user import GetUserRequest, ShowUser
from db.models import User



@pytest.fixture(scope="module")
def prepare_valid_test_data():
    return {
        "id": None,
        "name": "Artur",
        "username": "argen7um",
        "email": "argen7um@mail.com",
        "hashed_password": "tespass",
        "is_active": True,
    }


async def insert_test_user_into_db(test_data: dict, session: AsyncSession):
    test_user = User(**test_data)
    session.add(test_user)
    await session.flush()
    return test_user


@pytest.mark.asyncio
async def test_get_user_by_id(_get_test_db: AsyncSession, 
                              prepare_valid_test_data: dict[str, str]):

    async with _get_test_db as session:
        test_user = await insert_test_user_into_db(prepare_valid_test_data, session)
        
        assert True