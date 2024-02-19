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
    UnknownFieldsExeption,
    UserNotFoundExeption,
    MashupNotFoundExeption,
    SourceNotFoundExeption,
)


async def _create_mashup(
    body: CreateMashupRequest, session: AsyncSession
) -> ShowMashupWithRel:
    user_id = body.user_id
    user_dal = UserDAL(session)
    user = await user_dal.is_exists(user_id)

    audio = body.audio

    if not user:
        raise UserNotFoundExeption

    getted_sources_ids = body.sources_ids
    source_dal = SourceDAL(session)
    sources = []
    for source_id in getted_sources_ids:
        source = await source_dal.is_exists(source_id)
        if source:
            sources.append(source)
        else:
            SourceNotFoundExeption()

    mashup_dal = MashupDAL(session)
    created_mashup = await mashup_dal.create_mashup(
        name=body.name, 
        audio=audio, 
        user_id=user_id, 
        user=user, 
        sources=sources
    )
    return created_mashup.to_schema_with_rel()


async def _get_mashup(
    body: GetMashupRequest, session: AsyncSession
) -> List[ShowMashup]:
    mashup_dal = MashupDAL(session)

    if mashup_id := body.get("mashup_id"):
        getted_mashups = [(await mashup_dal.get_by_id(mashup_id))]
    elif name := body.get("name"):
        getted_mashups = [(mashup_dal.get_mashups_by_name(name))]
    elif user_id := body.get("user_id"):
        getted_mashups = mashup_dal.get_mashups_by_user_id(user_id)
    elif source_id := body.get("source_id"):
        getted_mashups = mashup_dal.get_mashups_by_source_id(source_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown fields in body data",
        )

    return [
        ShowMashup(
            mashup_id=mashup.mashup_id,
            name=mashup.name,
            user_id=mashup.user_id,
            source=[source.source_id for source in mashup.sources],
        )
        for mashup in getted_mashups
    ]


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
