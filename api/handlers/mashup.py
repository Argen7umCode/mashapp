from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from api.actions.mashup import _get_mashup


mashup_router = APIRouter(prefix='/mashup', tags=['mashups'])

