import uuid
from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.friendship import Friendship
from app.models.friendship_status import FriendshipStatus
from app.repositories.base_repository import BaseRepo


class FriendshipRepository(BaseRepo[Friendship]):
    def __init__(self, db: AsyncSession):
        super().__init__(Friendship, db)

    async def create_request(
        self, from_user: uuid.UUID, to_user: uuid.UUID
    ) -> Optional[Friendship]:
        data = {
            "sender_id": from_user,
            "receiver_id": to_user,
            "status": FriendshipStatus.PENDING,
        }
        try:
            await self.create(data)
        except Exception as e:
            return None

    async def update_status(
        self,
        from_user: uuid.UUID,
        to_user: uuid.UUID,
        friendship_status: FriendshipStatus,
    ) -> Friendship:
        friendship = await self.get_friendship_between(from_user, to_user)
        if friendship is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Friendship does not exist",
            )
        data = {
            "sender_id": from_user,
            "receiver_id": to_user,
            "status": friendship_status,
        }
        db_friendship = await self.update(friendship.id, data)
        return db_friendship

    async def get_friendship_between(
        self, user_id_1: uuid.UUID, user_id_2: uuid.UUID
    ) -> Optional[Friendship]:
        query = select(self.model).where(
            or_(
                and_(
                    self.model.sender_id == user_id_1,
                    self.model.receiver_id == user_id_2,
                ),
                and_(
                    self.model.sender_id == user_id_2,
                    self.model.receiver_id == user_id_1,
                ),
            )
        )
        return await self.db.scalar(query)

    async def get_pending_requests(self, user_id: uuid.UUID) -> List[Friendship]:
        query = (
            select(self.model)
            .where(
                self.model.receiver_id == user_id,
                self.model.status == FriendshipStatus.PENDING,
            )
            .options(selectinload(self.model.sender))
        )
        result = await self.db.scalars(query)
        return list(result.all())

    async def get_friends_list(self, user_id: uuid.UUID) -> List[Friendship]:
        query = (
            select(self.model)
            .where(
                and_(
                    or_(
                        self.model.sender_id == user_id,
                        self.model.receiver_id == user_id,
                    )
                ),
                FriendshipStatus.ACCEPTED == self.model.status,
            )
            .options(selectinload(self.model.sender), selectinload(self.model.receiver))
        )
        result = await self.db.scalars(query)
        return list(result.all())
