import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from api.actions.user import _delete_user
from api.schemas.user import DeleteUserRequest, DeleteUserResponse
from exceptions.exceptions import UserAlreadyExistsExeption, UserNotFoundExeption
from tests.db_funcs import insert_into_db
from db.models import User


@pytest.mark.asyncio
async def test_sucssess_delete(
    _get_test_db: AsyncSession, prepare_valid_test_data: dict[str, str]
):
    test_user = User(**prepare_valid_test_data)
    async with _get_test_db as session:
        await insert_into_db(test_user, session)
        user_id = test_user.id

        request = DeleteUserRequest(id=user_id)

        delete_responce = await _delete_user(request, session)

        query = select(User).where(User.id == user_id)
        deleted_user = (await session.execute(query)).scalar_one_or_none()

    assert isinstance(delete_responce, DeleteUserResponse)
    assert deleted_user.id == user_id
    assert deleted_user.name == prepare_valid_test_data["name"]
    assert deleted_user.email == prepare_valid_test_data["email"]
    assert deleted_user.username == prepare_valid_test_data["username"]
    assert deleted_user.hashed_password == prepare_valid_test_data["hashed_password"]
    assert deleted_user.is_active == False


@pytest.mark.asyncio
async def test_delete_user_isnt_exist(
    _get_test_db: AsyncSession, prepare_valid_test_data: dict[str, str]
):
    user_id = 1
    async with _get_test_db as session:
        request = DeleteUserRequest(id=user_id)

        with pytest.raises(UserNotFoundExeption) as e:
            delete_responce = await _delete_user(request, session)
        assert e.value.detail == UserNotFoundExeption.detail
