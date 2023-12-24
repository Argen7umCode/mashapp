from typing import Optional, Union

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from db.dals import UserDAL, MashupDAL
from db.models import User
from api.schemas.user import CreateUserRequest, ShowUser, GetUserRequest, UpdateUserRequest
from api.schemas.user import UpdatedUserResponse, DeleteUserResponse, DeleteUserRequest


async def _create_user(body: CreateUserRequest, 
                       session: AsyncSession) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            name = body.name, 
            username = body.username,
            email = body.email,
            is_active = True,
            hashed_password = body.hashed_password
        )
    return ShowUser(user_id = user.user_id,
                    name = user.name,
                    username = user.username,
                    email = user.email,
                    is_active = user.is_active)


async def _get_user_by_id(user_id: UUID, 
                          session: AsyncSession) -> User:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_id(
            user_id = user_id,
        )

async def _get_user_by_mashup_id(mashup_id: UUID, 
                                 session: AsyncSession) -> User:
    async with session.begin():
        mashup_dal = MashupDAL(session)
        mashup = await mashup_dal.get_mashup_by_id(mashup_id)
        if mashup is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                detail = f'Mashup with id {mashup_id} not found.')
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_mashup_id(mashup_id = mashup_id)

async def _get_user_by_email(email: str, session: AsyncSession) -> User:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_email(
            email = email,
        )
    
async def _get_user(body: GetUserRequest,
                    session: AsyncSession) -> ShowUser:
    if user_id := body.get('user_id'):
        user = await _get_user_by_id(user_id, session)
    elif email := body.get('email'):
        user = await _get_user_by_email(email, session)
    elif mashup_id := body.get('mashup_id'):
        user = await _get_user_by_mashup_id(mashup_id, session)
    else: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = 'Unknown fields in body data',
        ) 
    
    if user in None: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, detail='User not found.'
        )
    
    return ShowUser(user_id = user.user_id,
                    name = user.name,
                    username = user.username,
                    email = user.email,
                    is_active = user.is_active)


async def _delete_user(body: DeleteUserRequest, 
                       session: AsyncSession) -> DeleteUserResponse:
    async with session.begin():
        user_dal = UserDAL(session)
        user_id = await user_dal.delete_user(body.user_id)
    
    return DeleteUserResponse(deleted_user_id =user_id)


async def _update_user(new_data: UpdateUserRequest, 
                       user_id: UUID, 
                       session: AsyncSession) -> UpdatedUserResponse:
    async with session.begin():
        user_dal = UserDAL(session)
        user_id =  await user_dal.update_user(user_id, **new_data)
    return UpdatedUserResponse(updated_user_id = user_id)

