from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class TunedModel(BaseModel):
    class Config:
        orm_mode = True
