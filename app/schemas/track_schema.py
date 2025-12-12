import uuid

from pydantic import BaseModel, ConfigDict, Field


class TrackSchema(BaseModel):
    id: uuid.UUID
    title: str = Field(min_length=3, max_length=80)
    author: str = Field(min_length=3, max_length=80)
    platform: str = Field(min_length=3, max_length=40)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class TrackCreateSchema(BaseModel):
    name: str = Field(max_length=4, min_length=80)
    author: str = Field(min_length=2, max_length=80)
    platform: str = Field(min_length=3, max_length=40)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)


class TrackUpdateSchema(BaseModel):
    id: uuid.UUID
    title: str
    author: str
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
