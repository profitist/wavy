from typing import AsyncGenerator, Annotated

from app.core.database import session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repository import Repository as UserRepository
from app.services.user_service import Service as UserService


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


async def get_user_repository(
    db: Annotated[AsyncSession, get_async_session],
) -> UserRepository:
    return UserRepository(db=db)


async def get_user_service(repo: Annotated[UserRepository, get_user_repository]):
    return UserService(repo=repo)
