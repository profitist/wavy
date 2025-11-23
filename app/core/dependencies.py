from typing import AsyncGenerator

from app.core.database import session_maker
from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
