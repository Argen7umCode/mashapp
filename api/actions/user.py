from typing import Union

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from db.dals import UserDAL, MashupDAL


async def _get_user_by_id(user_id: UUID, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id,
        )
        return user

async def _get_user_by_mashup_id(mashup_id: UUID, session: AsyncSession):
    async with session.begin():
        mashup_dal = MashupDAL(session)
        mashup = await mashup_dal.get_mashup_by_id(mashup_id)
        if mashup is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f'Mashup with id {mashup_id} not found.')
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_mashup_id(mashup_id=mashup_id)
        return user

async def _get_user_by_email(email: str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_email(
            email=email,
        )
        return user
    
async def _delete_user(user_id: UUID, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        user_id = await user_dal.delete_user(user_id)


async def _update_user(new_data: dict, user_id: UUID, session: AsyncSession) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(user_id, **new_data)
        return updated_user_id
