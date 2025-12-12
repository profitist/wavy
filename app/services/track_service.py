import uuid
from typing import List

from fastapi import HTTPException, status

from app.core.s3 import S3Client
from app.models.track import Track
from app.models.user import User
from app.repositories.track_repository import TrackRepository
from app.schemas.track_schema import TrackCreateSchema, TrackUpdateSchema, TrackSchema


class TrackService:
    def __init__(self, repo: TrackRepository, s3_client: S3Client):
        self.repo = repo
        self.s3_client = s3_client

    async def get_by_id(self, track_id: uuid.UUID) -> Track:
        result = await self.repo.get_by_id(track_id)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Track not found",
            )
        return result

    async def create_track(self, track: TrackCreateSchema) -> Track:
        db_track = await self.repo.create(dict(track))
        return db_track

    async def get_tracks_by_details(
        self, title: str, author: str, offset: int = 0, limit: int = 20
    ) -> List[Track]:
        db_tracks = await self.repo.get_tracks_by_details(
            title=title, author=author, offset=offset, limit=limit
        )
        return db_tracks

    async def search_tracks(
        self, search_query: str, offset: int = 0, limit: int = 20
    ) -> List[Track]:
        result = await self.repo.search_track(search_query, offset=offset, limit=limit)
        return result

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

    async def save_song_cover(self, cover: bytes, filename: str) -> Track:
        await self.s3_client.upload_bytes(cover, filename)

    async def get_cover(self, id: str) -> bytes:
        song_cover = await self.s3_client.download_bytes(f"{id}.png")
        return song_cover
