from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.track import Track
from app.repositories.base_repository import BaseRepo


class TrackRepository(BaseRepo[Track]):
    def __init__(self, db: AsyncSession):
        super().__init__(Track, db)

    async def get_track_by_details(
        self, title: str, author: str, offset: int, limit: int
    ) -> List[Track]:
        filters = []
        if title is not None:
            filters.append(Track.title == title)
        if author is not None:
            filters.append(Track.author == author)
        query = select(self.model).where(*filters).offset(offset).limit(limit)
        return list((await self.db.scalars(query)).all())

    async def get_track_by_link(self, external_link: str) -> Optional[Track]:
        query = select(self.model).where(self.model.external_link == external_link)
        return await self.db.scalar(query)
