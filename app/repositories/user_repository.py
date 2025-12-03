from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base_repository import BaseRepo


class UserRepository(BaseRepo[User]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_username(self, username: str) -> Optional[User]:
        query = select(self.model).where(self.model.username == username)
        return await self.db.scalar(query)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(self.model).where(self.model.username == email)
        return await self.db.scalar(query)
