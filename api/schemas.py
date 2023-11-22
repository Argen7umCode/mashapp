from uuid import UUID
from pydantic import BaseModel, EmailStr


class TunedModel(BaseModel):
    class Config:
        orm_mode = True
        

class ShowUser(TunedModel):
    user_id: UUID
    name: str
    username: str
    email: EmailStr
    is_active: bool
