from typing import List
from api.schemas import TunedModel
from api.schemas import Optional, BaseModel


class CreateMashupRequest(TunedModel):
    name: str
    audio: bytes
    user_id: int
    sources: List[int]


class GetMashupRequest(TunedModel):
    mashup_id: Optional[int] = None
    name: Optional[str] = None
    user_id: Optional[int] = None
    source_id: Optional[int] = None


class ShowMashup(TunedModel):
    mashup_id: int
    name: str
    audio_id: int
    is_active: bool
    user_id: int
    sources_ids: List[int]


class ShowMashups(TunedModel):
    mashups: List[ShowMashup]


class UpdateMashupRequest(BaseModel):
    name: str
    audio: bytes


class UpdateMashupResponse(BaseModel):
    updated_mashup_id: int


class DeleteMashupRequest(BaseModel):
    mashup_id: int


class DeleteMahsupResponse(BaseModel):
    deleted_mashup_id: int
