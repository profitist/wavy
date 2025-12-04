import uuid
from typing import List

from fastapi import HTTPException, status

from app.models.track import Track
from app.models.user import User
from app.repositories.track_repository import TrackRepository
from app.schemas.track_schema import TrackCreateSchema, TrackUpdateSchema, TrackSchema


class TrackService:
    def __init__(self, repo: TrackRepository):
        self.repo = repo

    async def get_by_id(self, track_id: uuid.UUID) -> Track:
        result = await self.repo.get_by_id(track_id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Track not found",
            )
        return result

    async def get_tracks(self, offset: int, limit: int) -> List[Track]:
        tracks = await self.repo.get_all(skip=offset, limit=limit)
        return tracks

    async def create_track(self, track: TrackCreateSchema) -> Track:
        db_track = await self.repo.create(dict(track))
        return db_track

    async def get_tracks_by_name(self, name: str) -> List[Track]:
        db_tracks = await self.repo.get_track_by_name(name)
        return db_tracks

    async def edit_track_info(
        self, track_id: uuid.UUID, track: TrackUpdateSchema
    ) -> Track:
        db_track = await self.repo.get_by_id(track_id)
        if db_track is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Track not found"
            )
        return await self.repo.update(track_id, dict(track))

    async def delete_track(self, track_id: uuid.UUID) -> dict:
        db_track = await self.repo.get_by_id(track_id)
        if db_track is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Track not found"
            )
        await self.repo.delete(track_id)
        return {f"info": TrackSchema.from_orm(db_track), "message": "Track deleted"}
