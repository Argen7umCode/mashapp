import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from api.actions.mashup import _create_mashup
from api.schemas.mashup import CreateMashupRequest, ShowMashup
from tests.db_funcs import insert_into_db
from db.models import User, Mashup
