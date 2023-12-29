from api.schemas import TunedModel
from api.schemas import Optional, BaseModel


class CreateAudioRequest(TunedModel):
    audio: bytes


class GetAudioRequest(TunedModel):
    audio_id: Optional[int] = None
    mashup_id: Optional[int] = None


class ShowAudio(TunedModel):
    audio_id: int
    audio: bytes


class UpdateAudioRequest(BaseModel):
    audio: bytes


class UpdateAudioResponse(BaseModel):
    updated_audio_id: int


class DeleteAudioRequest(BaseModel):
    auido_id: int


class DeleteAudioResponse(BaseModel):
    deleted_audio_id: int
