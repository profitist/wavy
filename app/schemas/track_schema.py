import uuid

from pydantic import BaseModel, ConfigDict, Field


class TrackSchema(BaseModel):
    id: uuid.UUID
    name: str = Field(min_length=3, max_length=80)
    author: str = Field(min_length=3, max_length=80)
    album_cover_name: str = Field(min_length=3, max_length=150)
    music_platform: str = Field(min_length=3, max_length=40)

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class TrackCreateSchema(BaseModel):
    name: str = Field(max_length=40, min_length=80)
    author: str = Field(min_length=2, max_length=80)
    album_cover_name: str = Field(min_length=2, max_length=150)
    music_platform: str = Field(min_length=3, max_length=40)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class TrackUpdateSchema(BaseModel):
    id: uuid.UUID
    name: str
    author: str
    album_cover_name: str
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
