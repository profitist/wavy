import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.track import Track


class Repository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_track(self, track: Track) -> Track:
        self.db.add(track)
        await self.db.commit()
        await self.db.refresh(track)
        return track

    async def get_track_by_id(self, track_id: uuid.UUID) -> Optional[Track]:
        query = select(Track).where(Track.id == track_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_track_by_details(self, title: str, author: str) -> Optional[Track]:
        query = select(Track).where(
            (Track.title == title) & (Track.author == author)
        )
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_track_by_link(self, external_link: str) -> Optional[Track]:
        query = select(Track).where(Track.external_link == external_link)
        result = await self.db.execute(query)
        return result.scalars().first()