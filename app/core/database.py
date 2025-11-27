import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://username:password@localhost:5432/wavy."
)
engine = create_async_engine(DATABASE_URL, echo=True)

session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_session():
    async with session_maker() as session:
        yield session
