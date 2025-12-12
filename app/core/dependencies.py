from typing import AsyncGenerator, Annotated
from fastapi import Depends
from app.core.database import session_maker
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.friendship_repository import FriendshipRepository
from app.repositories.user_repository import UserRepository
from app.repositories.track_repository import TrackRepository
from app.repositories.shared_track_repository import SharedTrackRepository
from app.services.friendship_service import FriendshipService
from app.services.user_service import UserService
from app.services.track_service import TrackService
from app.services.sharing_service import SharingService
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


async def get_shared_track_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
):
    return SharedTrackRepository(db)


async def get_friendship_service(
    repo: Annotated[FriendshipRepository, Depends(get_friendship_repository)],
):
    return FriendshipService(repo=repo)


async def get_track_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
):
    return FriendshipRepository(db=db)


async def get_s3_client():
    return S3Client(
        access_key=S3_ID,
        secret_key=S3_SECRET,
        endpoint_url="https://storage.yandexcloud.net",
        bucket_name="storage-s3",
    )


async def get_track_service(
    repo: Annotated[TrackRepository, Depends(get_track_repository)],
    s3_client: Annotated[S3Client, Depends(get_s3_client)],
):
    return TrackService(repo=repo, s3_client=s3_client)


async def get_sharing_service(
    track_repo: Annotated[TrackRepository, Depends(get_track_repository)],
    share_repo: Annotated[SharedTrackRepository, Depends(get_shared_track_repository)],
) -> SharingService:
    return SharingService(track_repo=track_repo, share_repo=share_repo)
