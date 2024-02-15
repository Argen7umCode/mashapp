from typing import Optional, Union


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with same username or email is already exists",
        )
    return user.to_schema_without_rel()


async def _get_user_by_id(user_id: int, session: AsyncSession) -> User:
    user_dal = UserDAL(session)
    return await user_dal.get_by_id(
        user_id=user_id,
    )


async def _get_user_by_mashup_id(mashup_id: int, session: AsyncSession) -> User:
    mashup_dal = MashupDAL(session)
    mashup = await mashup_dal.get_by_id(mashup_id)
    if mashup is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mashup with id {mashup_id} not found.",
        )
    user_dal = UserDAL(session)
    return await user_dal.get_user_by_mashup_id(mashup_id=mashup_id)


async def _get_user_by_email(email: str, session: AsyncSession) -> User:
    user_dal = UserDAL(session)
    return await user_dal.get_user_by_email(
        email=email,
    )


async def _get_user(body: GetUserRequest, session: AsyncSession) -> ShowUser:
    if user_id := body.id:
        user = await _get_user_by_id(user_id, session)
    elif email := body.email:
        user = await _get_user_by_email(email, session)
    elif mashup_id := body.mashup_id:
        user = await _get_user_by_mashup_id(mashup_id, session)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown fields in body data",
        )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return user.to_schema_without_rel()


async def _delete_user(
    body: DeleteUserRequest, session: AsyncSession
) -> DeleteUserResponse:
    user_dal = UserDAL(session)
    user_id = await user_dal.delete_user(body.user_id)

    return DeleteUserResponse(deleted_user_id=user_id)


async def _update_user(
    new_data: UpdateUserRequest, user_id: int, session: AsyncSession
) -> UpdatedUserResponse:
    user_dal = UserDAL(session)
    cleared_data = remove_none_values_from_dict(dict(new_data))
    user_id = await user_dal.update_user(user_id, **cleared_data)
    return UpdatedUserResponse(id=user_id)
