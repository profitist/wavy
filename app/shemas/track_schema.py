import uuid

from pydantic import BaseModel


class TrackSchema(BaseModel):
    id: uuid.UUID
    name: str
    author: str
    album_cover_url: str
    music_platform: str


class TrackCreateSchema(BaseModel):
    name: str
    author: str
    album_cover_url: str
    music_platform: str
