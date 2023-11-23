from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, constr


class TunedModel(BaseModel):
    class Config:
        orm_mode = True
        