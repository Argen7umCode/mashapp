from typing import TYPE_CHECKING, Optional, List

from api.schemas import BaseModel

if TYPE_CHECKING:
    from api.schemas.mashup import ShowMashup
    from api.schemas.author import ShowAuthor


class CreateSourceRequest(BaseModel):
    name: str
    authors: List[int]


class ShowSource(BaseModel):
    id: int
    name: str
    audio: bytes
    is_active: bool


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
