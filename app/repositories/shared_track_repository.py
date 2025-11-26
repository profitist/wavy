import uuid
from typing import List

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.shared_track import SharedTrack
from app.repositories.base_repository import BaseRepo


class SharedTrackRepository(BaseRepo[SharedTrack]):
    def __init__(self, db: AsyncSession):
        super().__init__(SharedTrack, db)

    async def get_last_tracks_feed(self, user_ids: List[uuid.UUID], limit: int = 20, offset: int = 0) -> List[SharedTrack]:
        if not user_ids:
            return []

        query = select(self.model).where(self.model.sender_id.in_(user_ids)) \
            .order_by(desc(self.model.created_at)).limit(limit).offset(offset).options(
            selectinload(self.model.track),
            selectinload(self.model.sender),
            selectinload(self.model.reactions)
            .selectinload("user")
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_shared_tracks_by_user(self, user_id: uuid.UUID, limit: int = 20, offset: int = 0) -> List[SharedTrack]:
        query = select(self.model) \
            .where(self.model.sender_id == user_id).order_by(desc(self.model.created_at)) \
            .limit(limit).offset(offset).options(
            selectinload(self.model.track),
            selectinload(self.model.reactions)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())