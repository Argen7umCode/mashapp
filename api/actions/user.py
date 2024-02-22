from typing import List, Optional, Union


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from api.schemas.relationships import ShowUserWithRel

from db.dals import UserDAL, MashupDAL
from db.models import User
from api.schemas.user import (
    CreateUserRequest,
    ShowUser,
    GetUserRequest,
    UpdateUserRequest,
)
from api.schemas.user import UpdatedUserResponse, DeleteUserResponse, DeleteUserRequest
from api.actions.common import remove_none_values_from_dict
from exceptions.exceptions import (
    MashupNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
    UnknownFieldsException,
)


async def _create_user(body: CreateUserRequest, session: AsyncSession) -> ShowUser:
    user_dal = UserDAL(session)

    try:
        user = await user_dal.create_user(
            name=body.name,
            username=body.username,
            email=body.email,
            is_active=True,
            hashed_password=body.hashed_password,
        )
    except IntegrityError:
        raise UserAlreadyExistsException()
    else:
        return user.to_schema_without_rel()


async def _get_user_by_id(user_id: int, session: AsyncSession) -> User:
    user_dal = UserDAL(session)
    return await user_dal.get_by_id(
        user_id=user_id,
    )


async def _get_users(
    body: GetUserRequest, session: AsyncSession
) -> List[ShowUserWithRel]:
    if user_id := body.id:
        users = [await _get_user_by_id(user_id, session)]
    else:
        clean_body = remove_none_values_from_dict(dict(body))
        user_dal = UserDAL(session)
        users = await user_dal.get(clean_body)
    
    if not all(users) or len(users) == 0:
        raise UserNotFoundException()

    return [user.to_schema_with_rel() for user in users]


async def _delete_user(
    body: DeleteUserRequest, session: AsyncSession
) -> DeleteUserResponse:
    user_dal = UserDAL(session)
    user_id = await user_dal.delete_user(body.id)

    if user_id is None:
        raise UserNotFoundException()

    return DeleteUserResponse(id=user_id)


async def _update_user(
    new_data: UpdateUserRequest, user_id: int, session: AsyncSession
) -> UpdatedUserResponse:
    user_dal = UserDAL(session)
    cleared_data = remove_none_values_from_dict(dict(new_data))

    try:
        user_id = await user_dal.update_user(user_id, **cleared_data)
    except ValueError:
        raise UnknownFieldsException()

    if user_id is None:
        raise UserNotFoundException()

    return UpdatedUserResponse(id=user_id)
