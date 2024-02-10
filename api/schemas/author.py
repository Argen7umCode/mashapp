from typing import TYPE_CHECKING, Optional, List

from api.schemas import BaseModel, TunedModel


if TYPE_CHECKING:
    from api.schemas.source import ShowSource


class CreateAuthor(BaseModel):
    id: int
    name: str


class ShowAuthor(BaseModel):
    id: int
    name: str
    is_active: bool


class ShowAuthorWithRel(ShowAuthor):
    sources: "List[ShowSource]"


class GetAuthorRequest(BaseModel):
    id: Optional[int]
    name: Optional[str]
    source_id: Optional[int]


class UpdateAuthorRequest(BaseModel):
    id: Optional[int]
    name: Optional[str]


class UpdateAuthorResponse(BaseModel):
    id: int


class DeleteAuthorRequest(BaseModel):
    id: int


class DeleteAuthorResponse(BaseModel):
    id: int
