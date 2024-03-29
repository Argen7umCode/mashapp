import pytest


from api.actions.user import (
    _create_user,
)

from sqlalchemy import and_, select

from fastapi import HTTPException, status
from api.schemas.user import CreateUserRequest, ShowUser
from exceptions.exceptions import UserAlreadyExistsException
from db.models import User


@pytest.mark.asyncio
async def test_create_user_succsses_insert_into_db(
    _get_test_db, prepare_valid_test_data
):
    name = prepare_valid_test_data["name"]
    username = prepare_valid_test_data["username"]
    email = prepare_valid_test_data["email"]
    hashed_password = prepare_valid_test_data["hashed_password"]

    async with _get_test_db as session:
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
        test = db_response.scalar().to_schema_without_rel()

        assert response.name == test.name
        assert response.username == test.username
        assert response.email == test.email


@pytest.mark.asyncio
async def test_create_user_return_valid_data(_get_test_db, prepare_valid_test_data):
    name = prepare_valid_test_data["name"]
    username = prepare_valid_test_data["username"]
    email = prepare_valid_test_data["email"]
    hashed_password = prepare_valid_test_data["hashed_password"]

    async with _get_test_db as session:
        user_data = CreateUserRequest(
            name=name, username=username, email=email, hashed_password=hashed_password
        )

        response = await _create_user(user_data, session)

    assert response.name == name
    assert response.username == username
    assert response.email == email
    assert isinstance(response, ShowUser)


@pytest.mark.asyncio
async def test_duplicate_data(_get_test_db, prepare_valid_test_data):
    name = prepare_valid_test_data["name"]
    username = prepare_valid_test_data["username"]
    email = prepare_valid_test_data["email"]
    hashed_password = prepare_valid_test_data["hashed_password"]

    async with _get_test_db as session:
        user_data = CreateUserRequest(
            name=name, username=username, email=email, hashed_password=hashed_password
        )

        response = await _create_user(user_data, session)

        with pytest.raises(UserAlreadyExistsException) as e:
            second_response = await _create_user(user_data, session)
        assert e.value.detail == UserAlreadyExistsException.detail
