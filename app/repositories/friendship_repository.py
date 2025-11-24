import uuid
from typing import Optional, List
from sqlalchemy import select, or_, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.friendship import Friendship
from app.models.friendship_status import FriendshipStatus


class Repository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_friendship(self, friendship: Friendship) -> Friendship:
        self.db.add(friendship)
        await self.db.commit()
        await self.db.refresh(friendship)
        return friendship

    async def get_friendship_between(self, user_id_1: uuid.UUID, user_id_2: uuid.UUID) -> Optional[Friendship]:
        query = select(Friendship).where(or_(
                and_(Friendship.sender_id == user_id_1, Friendship.receiver_id == user_id_2),
                and_(Friendship.sender_id == user_id_2, Friendship.receiver_id == user_id_1)
            )
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_pending_requests(self, user_id: uuid.UUID) -> List[Friendship]:
        query = select(Friendship).where(
            (Friendship.receiver_id == user_id) & (Friendship.status == FriendshipStatus.PENDING)
        ).options(selectinload(Friendship.sender))
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_status(self, friendship: Friendship, new_status: FriendshipStatus) -> Friendship:
        friendship.status = new_status
        self.db.add(friendship)
        await self.db.commit()
        await self.db.refresh(friendship)
        return friendship

    async def delete_friendship(self, friendship_id: uuid.UUID) -> bool:
        query = delete(Friendship).where(Friendship.id == friendship_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
