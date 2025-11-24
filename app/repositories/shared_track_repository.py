import uuid
from typing import List, Optional

from sqlalchemy import select, delete, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.shared_track import SharedTrack


class Repository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_share(self, shared_track: SharedTrack) -> SharedTrack:
        self.db.add(shared_track)
        await self.db.commit()
        await self.db.refresh(shared_track)
        return shared_track

    async def get_by_id(self, share_id: uuid.UUID) -> Optional[SharedTrack]:
        query = select(SharedTrack).where(SharedTrack.id == share_id).options(
            selectinload(SharedTrack.track),
            selectinload(SharedTrack.sender),
            selectinload(SharedTrack.reactions)
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_feed_by_user_ids(self, user_ids: List[uuid.UUID], limit: int = 20, offset: int = 0) -> List[
        SharedTrack]:
        if not user_ids:
            return []
        query = select(SharedTrack).where(SharedTrack.sender_id.in_(user_ids)) \
            .order_by(desc(SharedTrack.created_at)).limit(limit) \
            .offset(offset).options(
            selectinload(SharedTrack.track),
            selectinload(SharedTrack.sender),
            selectinload(SharedTrack.reactions).selectinload("user")
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_shares_by_user(self, user_id: uuid.UUID, limit: int = 20, offset: int = 0) -> List[SharedTrack]:
        query = select(SharedTrack).where(SharedTrack.sender_id == user_id) \
            .order_by(desc(SharedTrack.created_at)).limit(limit) \
            .offset(offset).options(
            selectinload(SharedTrack.track),
            selectinload(SharedTrack.reactions)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update_share_description(self, shared_track: SharedTrack, new_description: str) -> SharedTrack:
        shared_track.description = new_description
        self.db.add(shared_track)
        await self.db.commit()
        await self.db.refresh(shared_track)
        return shared_track

    async def delete_share(self, share_id: uuid.UUID) -> bool:
        query = delete(SharedTrack).where(SharedTrack.id == share_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
