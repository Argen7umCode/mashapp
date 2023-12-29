from typing import TYPE_CHECKING, List
from api.schemas import TunedModel
from api.schemas import Optional, BaseModel


if TYPE_CHECKING:
    from api.schemas.user import ShowUser
    from api.schemas.source import ShowSource


class CreateMashupRequest(TunedModel):
    name: str
    audio: bytes
    user_id: int
    sources: List[int]


class GetMashupRequest(TunedModel):
    id: Optional[int] = None
    name: Optional[str] = None
    user_id: Optional[int] = None
    source_id: Optional[int] = None


class ShowMashup(TunedModel):
    id: int
    name: str
    audio_id: int
    is_active: bool


class ShowMashupWithRel(ShowMashup):
    user: "ShowUser"
    sources: "List[ShowSource]"


class UpdateMashupRequest(BaseModel):
    name: str
    audio: bytes


class UpdateMashupResponse(BaseModel):
    id: int


class DeleteMashupRequest(BaseModel):
    id: int


class DeleteMahsupResponse(BaseModel):
    id: int
