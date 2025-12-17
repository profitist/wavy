import uuid
from typing import Optional, List, Mapping

from fastapi import HTTPException, status
from sqlalchemy import select, or_, and_, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, aliased

from app.models import User
from app.models.friendship import Friendship
from app.models.friendship_status import FriendshipStatus
from app.repositories.base_repository import BaseRepo


class FriendshipRepository(BaseRepo[Friendship]):
    def __init__(self, db: AsyncSession):
        super().__init__(Friendship, db)

    async def create_request(
        self, from_user: uuid.UUID, to_user: uuid.UUID
    ) -> Optional[Mapping]:
        stmt = (
            insert(self.model)
            .values(
                sender_id=from_user,
                receiver_id=to_user,
                status=FriendshipStatus.PENDING,
            )
            .returning(self.model)
        )
        try:
            result = await self.db.execute(stmt)
            await self.db.commit()
            return result.mappings().first()
        except Exception:
            await self.db.rollback()
            return None

    async def update_status(
        self,
        from_user: uuid.UUID,
        to_user: uuid.UUID,
        friendship_status: FriendshipStatus,
    ) -> Mapping:
        stmt = (
            update(self.model)
            .where(
                or_(
                    and_(
                        self.model.c.sender_id == from_user,
                        self.model.c.receiver_id == to_user,
                    ),
                    and_(
                        self.model.c.sender_id == to_user,
                        self.model.c.receiver_id == from_user,
                    ),
                )
            )
            .values(status=friendship_status)
            .returning(self.model)
        )
        result = await self.db.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Friendship does not exist",
            )
        await self.db.commit()
        return result.mappings().first()

    async def get_friendship_info_between(
        self, user_id_1: uuid.UUID, user_id_2: uuid.UUID
    ) -> Optional[Mapping]:
        stmt = select(self.model).where(
            or_(
                and_(
                    self.model.c.sender_id == user_id_1,
                    self.model.c.receiver_id == user_id_2,
                ),
                and_(
                    self.model.c.sender_id == user_id_2,
                    self.model.c.receiver_id == user_id_1,
                ),
            )
        )

        result = await self.db.execute(stmt)
        return result.mappings().first()

    async def get_requests_with_status(
        self, user_id: uuid.UUID, friendship_status: FriendshipStatus
    ) -> list[dict]:
        sender_alias = aliased(User)
        receiver_alias = aliased(User)

        stmt = (
            select(
                Friendship.c.id.label("friendship_id"),
                sender_alias.id.label("sender_id"),
                sender_alias.username.label("sender_username"),
                sender_alias.description.label("sender_description"),
                sender_alias.phone_number.label("sender_phone_number"),
                sender_alias.profile_picture_url.label("sender_profile_picture_url"),
                receiver_alias.id.label("receiver_id"),
                receiver_alias.username.label("receiver_username"),
                receiver_alias.description.label("receiver_description"),
                receiver_alias.phone_number.label("receiver_phone_number"),
                receiver_alias.profile_picture_url.label(
                    "receiver_profile_picture_url"
                ),
            )
            .join(sender_alias, Friendship.c.sender_id == sender_alias.id)
            .join(receiver_alias, Friendship.c.receiver_id == receiver_alias.id)
            .where(
                or_(
                    and_(
                        Friendship.c.receiver_id == user_id,
                        Friendship.c.status == friendship_status,
                    ),
                    and_(
                        Friendship.c.sender_id == user_id,
                        Friendship.c.status == friendship_status,
                    ),
                )
            )
        )

        result = await self.db.execute(stmt)
        pending_requests = []

        for row in result.all():
            friendship_dict = {
                "friendship_id": row.friendship_id,
                "sender": {
                    "id": row.sender_id,
                    "username": row.sender_username,
                    "description": row.sender_description,
                    "phone_number": row.sender_phone_number,
                    "profile_picture_url": row.sender_profile_picture_url,
                },
                "receiver": {
                    "id": row.receiver_id,
                    "username": row.receiver_username,
                    "description": row.receiver_description,
                    "phone_number": row.receiver_phone_number,
                    "profile_picture_url": row.receiver_profile_picture_url,
                },
                "status": FriendshipStatus.PENDING,
            }
            pending_requests.append(friendship_dict)

        return pending_requests
