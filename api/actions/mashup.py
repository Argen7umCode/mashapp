from typing import Optional, Union

from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from db.dals import MashupDAL, UserDAL, AudioDAL
from api.schemas.mashup import CreateMashupRequest, ShowMashup, GetMashupRequest
from api.schemas.mashup import UpdateMashupRequest, UpdateMashupResponse
from api.schemas.mashup import DeleteMahsupResponse, DeleteMashupRequest


async def _create_mashup(body: CreateMashupRequest, 
                         session: AsyncSession) -> ShowMashup:
    with session.begin():
        user_id = body.user_id
        user_dal = UserDAL(session)
        if not await user_dal.id_user_exists(user_id):
            pass
        
        
        mashup_dal = MashupDAL(session)

