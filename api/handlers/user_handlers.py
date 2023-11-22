from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from api.schemas import ShowUser
from api.actions.user import _get_user_by_id


user_router = APIRouter(prefix='/users', tags=['users'])


@user_router.get('get_by_id/', response_model=ShowUser)
async def get_user_by_id(user_id: UUID, 
                         db: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user in None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'User with id {id} not found.')
    
