from typing import List, TYPE_CHECKING

from api.schemas import EmailStr
from api.schemas import Optional, BaseModel, constr


if TYPE_CHECKING:
    from api.schemas.mashup import ShowMashup


class CreateUserRequest(BaseModel):
    name: str
    username: str
    email: EmailStr
    hashed_password: str


class GetUserRequest(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
    mashup_id: Optional[int] = None


class ShowUser(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    is_active: bool


class UpdatedUserResponse(BaseModel):
    id: int


class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)] = None
    username: Optional[constr(min_length=1)] = None
    email: Optional[EmailStr] = None


class DeleteUserResponse(BaseModel):
    id: int


class DeleteUserRequest(BaseModel):
    id: int
