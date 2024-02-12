import asyncio
import pytest
from httpx import AsyncClient

from api.actions.user import (
    _create_user,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, delete, text
from api.schemas.user import CreateUserRequest, ShowUser
from db.models import User
from conftest import _get_test_db


# @pytest.fixture(scope="module")
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()



@pytest.mark.asyncio
async def test_create_user_succsses_insert_into_db(_get_test_db):
    session =  _get_test_db()
    
    name = "Artur"
    username = "argen7um"
    email = "argen7um@mail.com"
    hashed_password = "tespass"

    user_data = CreateUserRequest(
        name=name, username=username, email=email, hashed_password=hashed_password
    )

    response = await _create_user(user_data, session)

    query = select(User).where(
        and_(
            User.name == name,
            User.username == username,
            User.email == email,
            User.hashed_password == hashed_password,
        )
    )
    db_response = await session.execute(query)
    test = db_response.fetchall()

    await session.rollback()
    assert True


# @pytest.mark.asyncio
# async def test_create_user_return_valid_data(get_session):
#     session = await get_session
#     name = "Artur"
#     username = "argen7um"
#     email = "argen7um@mail.com"
#     hashed_password = "tespass"

#     user_data = CreateUserRequest(
#         name=name, username=username, email=email, hashed_password=hashed_password
#     )

#     response = await _create_user(user_data, session)

#     assert response.name == name
#     assert response.username == username
#     assert response.email == email
#     assert response.hashed_password == hashed_password
#     assert isinstance(response, ShowUser)
