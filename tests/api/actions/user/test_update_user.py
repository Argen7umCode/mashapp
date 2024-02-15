from typing import Any
import pytest


from api.actions.user import (
    _update_user,
)

from sqlalchemy import and_, select

from fastapi import HTTPException, status
from api.schemas.user import UpdateUserRequest, UpdatedUserResponse
from db.models import User
from tests.db_funcs import insert_into_db


updated_name = 'Pavel'
updated_username = 'aphexfan'
updated_email = "aphexfan@mail.com"


@pytest.fixture(scope="module")
def prepare_new_test_data() -> dict[str, Any]:
    return {
        "id": None,
        "name": "Pavel",
        "username": "aphexfan",
        "email": "aphexfan@mail.com",
        "hashed_password": "tespass",
        "is_active": True,
    }

@pytest.mark.parametrize("new_data", (({'name':updated_name},
                                       {'username':updated_username},
                                       {'email':updated_email},
                                       {'name':updated_name, 'email':updated_email},
                                       {'name':updated_name, 'username':updated_username},
                                       {'email':updated_email, 'username':updated_username},
                                       {'name':updated_name, 'email':updated_email, 'username':updated_username})))
@pytest.mark.asyncio
async def test_succsses_update_user(
    _get_test_db, prepare_valid_test_data, new_data
):
    name = prepare_valid_test_data["name"]
    username = prepare_valid_test_data["username"]
    email = prepare_valid_test_data["email"]
    hashed_password = prepare_valid_test_data["hashed_password"]

    async with _get_test_db as session:
        test_user = User(**prepare_valid_test_data)
        await insert_into_db(test_user, session)

        user_data = UpdateUserRequest(
            **new_data
        )
        updated_data = await _update_user(user_data, 
                                          test_user.id, 
                                          session)
        
        assert isinstance(updated_data, UpdatedUserResponse)
        assert updated_data.id == test_user.id

        query = select(User).where(User.id == test_user.id)
        updated_user = (await session.execute(query)).scalar_one_or_none()

        assert updated_user.id == test_user.id

        if new_name:=new_data.get('name'):
            assert updated_user.name == new_name 
        else:
            assert updated_user.name == test_user.name

        if new_username:=new_data.get('username'):
            assert updated_user.username == new_username 
        else:
            assert updated_user.username == test_user.username

        if new_email:=new_data.get('email'):
            assert updated_user.email == new_email 
        else:
            assert updated_user.email == test_user.email

        assert updated_user.hashed_password == test_user.hashed_password
        
        

