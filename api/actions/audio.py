from typing import Optional, Union


from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from db.dals import MashupDAL, UserDAL, AudioDAL
from api.schemas.audio import (
    CreateAudioRequest,
    GetAudioRequest,
    ShowAudio,
    UpdateAudioRequest,
)
from api.schemas.audio import (
    UpdateAudioResponse,
    DeleteAudioRequest,
    DeleteAudioResponse,
)


async def _create_audio(body: CreateAudioRequest, session: AsyncSession) -> ShowAudio:
    with session.begin():
        audio_dal = AudioDAL(session)
        audio = body.audio

        new_audio = await audio_dal.create_audio(audio)
        return ShowAudio(audio_id=new_audio.audio_id, audio=new_audio.audio)


async def _get_audio(body: GetAudioRequest, session: AsyncSession) -> ShowAudio:
    with session.begin():
        audio_dal = AudioDAL(session)
        if audio_id := body.get("audio_id"):
            getted_audio = await audio_dal.get_by_id(audio_id)
        elif mashup_id := body.get("mashup_id"):
            getted_audio = await audio_dal.get_audio_by_mashup_id(mashup_id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unknown fields in body data",
            )


async def _update_audio(
    audio_id: int, body: UpdateAudioRequest, session: AsyncSession
) -> UpdateAudioResponse:
    with session.begin():
        audio_dal = AudioDAL(session)
        audio_id = await audio_dal.update_audio(audio_id, **body)
    return UpdateAudioResponse(updated_audio_id=audio_id)


async def _delete_audio(
    body: DeleteAudioRequest, session: AsyncSession
) -> DeleteAudioResponse:
    with session.begin():
        audio_dal = AudioDAL(session)
        audio_id = await audio_dal.delete_audio(body.audio_id)
    return DeleteAudioResponse(deleted_audio_id=audio_id)
