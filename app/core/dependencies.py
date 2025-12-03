from typing import AsyncGenerator, Annotated
from fastapi import Depends
from app.core.database import session_maker
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.friendship_repository import FriendshipRepository
from app.repositories.user_repository import UserRepository
from app.services.friendship_service import FriendshipService
from app.services.user_service import UserService as UserService


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


async def get_user_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserRepository:
    return UserRepository(db=db)


async def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    return UserService(repo=repo)


async def get_friendship_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
):
    return FriendshipRepository(db=db)


async def get_friendship_service(
    repo: Annotated[FriendshipRepository, Depends(get_friendship_repository)],
):
    return FriendshipService(repo=repo)
