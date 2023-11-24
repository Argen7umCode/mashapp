from typing import List
from api.schemas import TunedModel, UUID 
from api.schemas import Optional, BaseModel



class CreateMashupRequest(TunedModel):
    name: str
    audio: bytes
    user_id: UUID
    sources: List[UUID]


class GetMashupRequest(TunedModel):
    mashup_id: Optional[UUID] = None
    name: Optional[str] = None
    user_id: Optional[UUID] = None
    source_id: Optional[UUID] = None


class ShowMashup(TunedModel):
    mashup_id: UUID
    name: str
    audio_id: UUID
    is_active: bool
    user_id: UUID
    sources_ids: List[UUID]

class ShowMashups(TunedModel):
    mashups: List[ShowMashup]



class UpdateMashupRequest(BaseModel):
    name: str
    audio: bytes

class UpdateMashupResponse(BaseModel):
    updated_mashup_id: UUID

class DeleteMashupRequest(BaseModel):
    mashup_id: UUID


class DeleteMahsupResponse(BaseModel):
    deleted_mashup_id: UUID
