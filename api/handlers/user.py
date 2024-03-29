from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db

from api.actions.user import _create_user, _get_users, _update_user, _delete_user
from api.schemas.user import (
    CreateUserRequest,
    ShowUser,
    GetUserRequest,
    UpdateUserRequest,
    UpdatedUserResponse,
    DeleteUserResponse,
    DeleteUserRequest,
)
from api.schemas.relationships import ShowUserWithRel


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/", response_model=ShowUser)
async def create_user(body: CreateUserRequest, db: AsyncSession = Depends(get_db)):
    return await _create_user(body, db)


@user_router.get("/", response_model=ShowUserWithRel)
async def get_users(
    body: GetUserRequest, db: AsyncSession = Depends(get_db)
) -> List[ShowUserWithRel]:
    return await _get_users(body, db)


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user(
    body: UpdateUserRequest, db: AsyncSession = Depends(get_db)
) -> UpdatedUserResponse:
    return await _update_user(body, db)


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    body: DeleteUserRequest, db: AsyncSession = Depends(get_db)
) -> DeleteUserResponse:
    return await _delete_user(body, db)
