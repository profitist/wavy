from typing import AsyncGenerator, Annotated
from fastapi import Depends
from app.core.database import session_maker
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.friendship_repository import FriendshipRepository
from app.repositories.user_repository import UserRepository
from app.repositories.track_repository import TrackRepository
from app.services.friendship_service import FriendshipService
from app.services.user_service import UserService
from app.services.track_service import TrackService
from app.core.s3 import S3Client
from app.config import S3_ID, S3_SECRET


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


async def get_track_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
):
    return FriendshipRepository(db=db)


async def get_s3_client():
    return S3Client(S3_ID, S3_SECRET, 'https://storage.yandexcloud.net', 'storage-s3')


async def get_track_service(
    repo: Annotated[TrackRepository, Depends(get_track_repository)],
    s3_client: Annotated[S3Client, Depends(get_s3_client)],
):
    return TrackService(repo=repo, s3_client=s3_client)
