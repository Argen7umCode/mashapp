from typing import List, TYPE_CHECKING

from api.schemas import TunedModel, EmailStr
from api.schemas import Optional, BaseModel, constr


if TYPE_CHECKING:
    from api.schemas.mashup import ShowMashup


class CreateUserRequest(TunedModel):
    name: str
    username: str
    email: EmailStr
    hashed_password: str


class GetUserRequest(TunedModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    mashup_id: Optional[int] = None


class ShowUser(TunedModel):
    id: int
    name: str
    username: str
    email: EmailStr
    is_active: bool


class ShowUserWithRel(ShowUser):
    mashups: "List[ShowMashup]"


class UpdatedUserResponse(BaseModel):
    id: int


class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]


class DeleteUserResponse(BaseModel):
    id: int


class DeleteUserRequest(BaseModel):
    id: int
