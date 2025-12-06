from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.track import Track
from app.repositories.base_repository import BaseRepo


class TrackRepository(BaseRepo[Track]):
    def __init__(self, db: AsyncSession):
        super().__init__(Track, db)

    async def get_track_by_details(self, title: str, author: str) -> Optional[Track]:
        query = select(self.model).where(
            (self.model.title == title) & (self.model.author == author)
        )
        return await self.db.scalar(query)

    async def get_track_by_link(self, external_link: str) -> Optional[Track]:
        query = select(self.model).where(self.model.external_link == external_link)
        return await self.db.scalar(query)

    async def get_track_by_name(self, track_name: str) -> List[Track]:
        query = select(self.model).where(self.model.title == track_name)
        result = await self.db.scalars(query)
        return list(result)
