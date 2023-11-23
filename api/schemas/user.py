from api.schemas import TunedModel, UUID, EmailStr 
from api.schemas import Optional, BaseModel, constr


class CreateUserRequest(TunedModel):
    user_id: UUID
    name: str
    username: str
    email: EmailStr
    hashed_password: str


class GetUserRequest(TunedModel):
    email: Optional[EmailStr] = None
    mashup_id: Optional[UUID] = None


class ShowUser(TunedModel):
    user_id: UUID
    name: str
    username: str
    email: EmailStr
    is_active: bool


class UpdatedUserResponse(BaseModel):
    updated_user_id: UUID


class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]


class DeleteUserResponse(BaseModel):
    deleted_user_id: UUID


class DeleteUserRequest(BaseModel):
    user_id: UUID

