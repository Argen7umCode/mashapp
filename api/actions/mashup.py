from typing import List, Optional, Union


from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from api.schemas.relationships import ShowMashupWithRel

from db.dals import MashupDAL, UserDAL, SourceDAL
from api.schemas.mashup import (
    CreateMashupRequest,
    ShowMashup,
    ShowMashup,
    GetMashupRequest,
)
from api.schemas.mashup import UpdateMashupRequest, UpdateMashupResponse
from api.schemas.mashup import DeleteMahsupResponse, DeleteMashupRequest
from exceptions.exceptions import (
    UnknownFieldsException,
    UserNotFoundException,
    MashupNotFoundException,
    SourceNotFoundException,
)


async def _create_mashup(
    body: CreateMashupRequest, session: AsyncSession
) -> ShowMashupWithRel:
    user_id = body.user_id
    user_dal = UserDAL(session)

    if not (user := (await user_dal.is_exists(user_id))):
        raise UserNotFoundException
    audio = body.audio

    getted_sources_ids = body.sources_ids
    source_dal = SourceDAL(session)

    sources = []
    for source_id in getted_sources_ids:
        source = await source_dal.is_exists(source_id)
        if source:
            sources.append(source)
        else:
            raise SourceNotFoundException()

    mashup_dal = MashupDAL(session)
    created_mashup = await mashup_dal.create_mashup(
        name=body.name, audio=audio, user_id=user_id, user=user, sources=sources
    )
    return created_mashup.to_schema_with_rel()


async def _get_mashups(
    body: GetMashupRequest, session: AsyncSession
) -> List[ShowMashupWithRel]:
    mashup_dal = MashupDAL(session)

    if mashup_id := body.id:
        getted_mashups = [(await mashup_dal.get_by_id(mashup_id))]
    else:
        getted_mashups = await mashup_dal.get(dict(body))
        if getted_mashups == []:
            raise MashupNotFoundException

    return [mashup.to_schema_with_rel() for mashup in getted_mashups]


async def _update_mashup(
    mashup_id: int, body: UpdateMashupRequest, session: AsyncSession
) -> UpdateMashupResponse:
    mashup_dal = MashupDAL(session)
    mashup_id = await mashup_dal.update_mashup(mashup_id, **body)
    return UpdateMashupResponse(updated_mashup_id=mashup_id)


async def _delete_mashup(
    body: DeleteMashupRequest, session: AsyncSession
) -> DeleteMahsupResponse:
    mashup_dal = MashupDAL(session)
    mashup_id = await mashup_dal.delete_mashup(body.mashup_id)
    return DeleteMahsupResponse(deleted_mashup_id=mashup_id)
