from typing import TYPE_CHECKING, Optional, List

from api.schemas import BaseModel, TunedModel

if TYPE_CHECKING:
    from api.schemas.mashup import ShowMashup
    from api.schemas.author import ShowAuthor


class CreateSourceRequest(TunedModel):
    name: str
    authors: List[int]


class ShowSource(BaseModel):
    id: int
    name: str
    audio: bytes
    is_active: bool


class ShowSourceWithRel(ShowSource):
    mashups: "List[ShowMashup]"
    author: "ShowAuthor"


class GetSourceRequest(BaseModel):
    id: Optional[int]
    name: Optional[str]
    mashup_id: Optional[int]
    author_id: Optional[int]


class UpdateSourceRequest(BaseModel):
    name: Optional[str]
    audio: Optional[bytes]


class UpdateSourceResponse(BaseModel):
    id: int


class DeleteSourceRequest(BaseModel):
    id: int


class DeleteSourceResponse(BaseModel):
    id: int
