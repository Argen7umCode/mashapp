from api.schemas import TunedModel, UUID 
from api.schemas import Optional, BaseModel


class CreateAudioRequest(TunedModel):
    audio: bytes


class GetAudioRequest(TunedModel):
    audio_id: Optional[UUID] = None
    mashup_id: Optional[UUID] = None

class ShowAudio(TunedModel):
    audio_id: UUID
    audio: bytes

class UpdateAudioRequest(BaseModel):
    audio: bytes

class UpdateAudioResponse(BaseModel):
    updated_audio_id: UUID

class DeleteAudioRequest(BaseModel):
    auido_id: UUID


class DeleteAudioResponse(BaseModel):
    deleted_audio_id: UUID
