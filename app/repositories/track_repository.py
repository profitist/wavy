from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.track import Track
from app.repositories.base_repository import BaseRepo


class TrackRepository(BaseRepo[Track]):
    def __init__(self, db: AsyncSession):
        super().__init__(Track, db)

    async def get_tracks_by_details(
        self, title: str | None, author: str | None, offset: int, limit: int
    ) -> List[Track]:
        filters = []
        if title is not None:
            filters.append(Track.title.ilike(f"%{title}%"))
        if author is not None:
            filters.append(Track.author.ilike(f"%{author}%"))
        query = select(self.model).where(*filters).offset(offset).limit(limit)
        response = await self.db.scalars(query)
        return list(response.all())

    async def get_track_by_link(self, external_link: str) -> Optional[Track]:
        query = select(self.model).where(self.model.external_link == external_link)
        return await self.db.scalar(query)

    async def get_track_by_name(self, track_name: str) -> List[Track]:
        query = select(self.model).where(self.model.title == track_name)
        result = await self.db.scalars(query)
        return list(result)
