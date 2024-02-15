from typing import Any
import pytest


from api.actions.user import _get_user

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from api.schemas.user import GetUserRequest, ShowUser
from tests.db_funcs import insert_into_db
from db.models import User, Mashup


@pytest.mark.asyncio
async def test_get_user_by_id(
    _get_test_db: AsyncSession, prepare_valid_test_data: dict[str, str]
):
    async with _get_test_db as session:
        test_user = User(**prepare_valid_test_data)
        await insert_into_db(test_user, session)
        user_id = test_user.id

        request = GetUserRequest(id=user_id)
        got_user = await _get_user(request, session)

    assert got_user.name == prepare_valid_test_data["name"]
    assert got_user.username == prepare_valid_test_data["username"]
    assert got_user.email == prepare_valid_test_data["email"]
    assert got_user.is_active == prepare_valid_test_data["is_active"]
    assert isinstance(got_user, ShowUser)


@pytest.mark.asyncio
async def test_get_user_by_email(
    _get_test_db: AsyncSession, prepare_valid_test_data: dict[str, str]
):
    async with _get_test_db as session:
        test_user = User(**prepare_valid_test_data)
        await insert_into_db(test_user, session)
        user_email = test_user.email

        request = GetUserRequest(email=user_email)
        got_user = await _get_user(request, session)

    assert got_user.name == prepare_valid_test_data["name"]
    assert got_user.username == prepare_valid_test_data["username"]
    assert got_user.email == prepare_valid_test_data["email"]
    assert got_user.is_active == prepare_valid_test_data["is_active"]
    assert isinstance(got_user, ShowUser)


@pytest.mark.asyncio
async def test_get_user_by_mashup_id(
    _get_test_db: AsyncSession, prepare_valid_test_data: dict[str, str]
):
    async with _get_test_db as session:
        test_user = User(**prepare_valid_test_data)
        await insert_into_db(test_user, session)

        test_mashup = Mashup(
            id=None,
            name="test",
            is_active=True,
            audio=bytes(1),
            user=test_user,
            user_id=test_user.id,
        )
        await insert_into_db(test_mashup, session)

        mashup_id = test_mashup.id
        request = GetUserRequest(mashup_id=mashup_id)
        got_user = await _get_user(request, session)

    assert got_user.name == prepare_valid_test_data["name"]
    assert got_user.username == prepare_valid_test_data["username"]
    assert got_user.email == prepare_valid_test_data["email"]
    assert got_user.is_active == prepare_valid_test_data["is_active"]
    assert isinstance(got_user, ShowUser)


@pytest.mark.asyncio
async def test_get_user_when_user_isnt_exists(
    _get_test_db: AsyncSession
):  
    user_id = 1
    request = GetUserRequest(id=user_id)
    async with _get_test_db as session:
        
        with pytest.raises(HTTPException) as e:
            got_user = await _get_user(request, session)
    assert e.value.status_code == status.HTTP_404_NOT_FOUND
    assert str(e.value.detail) == "User not found."


@pytest.mark.asyncio
async def test_get_user_when_mashup_isnt_exists(
    _get_test_db: AsyncSession
):  
    mashup_id = 1
    request = GetUserRequest(mashup_id=mashup_id)
    async with _get_test_db as session:

        with pytest.raises(HTTPException) as e:
            got_user = await _get_user(request, session)
    assert e.value.status_code == status.HTTP_404_NOT_FOUND
    assert str(e.value.detail) == f"Mashup with id {mashup_id} not found."


@pytest.mark.asyncio
async def test_get_user_with_empty_body(
    _get_test_db: AsyncSession
):
    async with _get_test_db as session:
        request = GetUserRequest()
        
        with pytest.raises(HTTPException) as e:
            got_user = await _get_user(request, session)
    assert e.value.status_code == status.HTTP_400_BAD_REQUEST
    assert str(e.value.detail) == "Unknown fields in body data"

