import uuid

from fastapi import Depends, APIRouter, Path, status
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.shemas.user_schema import UserSchema
from app.core.dependencies import get_async_session
from app.services.user_service import Service as UserService
from app.api.routers import tokens

# написать дописать методы
router = APIRouter(prefix="/user", tags=["user"])


@router.get("/{username}")
async def get_user(username=Annotated[str, Path(max_length=20, min_length=1)]):
    pass


@router.post("/")
async def create_user(
    user: UserSchema, db: Annotated[UserService, Depends(get_async_session)]
):
    pass


token_router = tokens.router
router.include_router(token_router)
