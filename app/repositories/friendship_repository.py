import uuid
from typing import Optional

from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.friendship import Friendship
from app.models.friendship_status import FriendshipStatus
from app.repositories.base_repository import BaseRepo


class FriendshipRepository(BaseRepo[Friendship]):
    def __init__(self, db: AsyncSession):
        super().__init__(Friendship, db)

    async def get_status_between(self, user_id_1: uuid.UUID, user_id_2: uuid.UUID) -> Optional[Friendship]:
        query = select(self.model).where(or_(
                and_(self.model.sender_id == user_id_1, self.model.receiver_id == user_id_2),
                and_(self.model.sender_id == user_id_2, self.model.receiver_id == user_id_1)
            )
        )
        return await self.db.scalar(query)

    async def get_pending_requests(self, user_id: uuid.UUID) -> list[Friendship]:
        query = (select(self.model).where(
            (self.model.receiver_id == user_id) & (self.model.status == FriendshipStatus.PENDING))
                 .options(selectinload(self.model.sender)))
        await self.db.execute(query)
        return self.db.scalars().all()



    async def get_friends_list(self, user_id: uuid.UUID) -> list[Friendship]:
        query = select(self.model).where(
            ((self.model.sender_id == user_id) | (self.model.receiver_id == user_id)) &
            (self.model.status == FriendshipStatus.ACCEPTED)
        ).options(selectinload(self.model.sender), selectinload(self.model.receiver))
        await self.db.execute(query)
        return self.db.scalars().all()


