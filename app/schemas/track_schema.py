import uuid

from pydantic import BaseModel, ConfigDict, Field


class TrackSchema(BaseModel):
    id: uuid.UUID
    title: str = Field(min_length=1, max_length=80)
    author: str = Field(min_length=1, max_length=80)
    platform: str = Field(min_length=1, max_length=40, default="unknown")
    external_link: str = Field(min_length=1, max_length=200)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class TrackCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=80)
    author: str = Field(min_length=1, max_length=80)
    platform: str = Field(min_length=3, max_length=40, default="unknown")
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class TrackDataBaseCreate(TrackCreateSchema):
    external_link: str = Field(min_length=3, max_length=200)


class TrackUpdateSchema(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
