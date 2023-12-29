from api.schemas import TunedModel, EmailStr
from api.schemas import Optional, BaseModel, constr


class CreateUserRequest(TunedModel):
    user_id: int
    name: str
    username: str
    email: EmailStr
    hashed_password: str


class GetUserRequest(TunedModel):
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None
    mashup_id: Optional[int] = None


class ShowUser(TunedModel):
    user_id: int
    name: str
    username: str
    email: EmailStr
    is_active: bool


class UpdatedUserResponse(BaseModel):
    updated_user_id: int


class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]


class DeleteUserResponse(BaseModel):
    deleted_user_id: int


class DeleteUserRequest(BaseModel):
    user_id: int
