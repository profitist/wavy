import uuid

from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

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
        pass

    async def get_user_by_username(self, username: str) -> User:
        pass

    async def create_user(self, user: User) -> User:
        pass

    async def update_user(self, user: User) -> User:
        pass
