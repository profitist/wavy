import uuid

from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.dependencies import get_async_session
from app.models.user import User


class Repository:
    """
    Репозиторий работы с бд для юзера / степа тут надо
    написать все запросики через self.db
    """

    def __init__(self, db: Annotated[AsyncSession, get_async_session]):
        self.db = db

    async def get_user_by_uuid(self, user_id: uuid.UUID) -> User:
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> User:
        query = select(User).where(User.username == username)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        try:
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            await self.db.rollback()
            raise e

    async def update_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: uuid.UUID) -> bool:
        user = await self.get_user_by_uuid(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
            return True
        return False