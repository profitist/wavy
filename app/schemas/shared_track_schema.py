import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.track_schema import TrackCreateSchema, TrackSchema


class ShareRequestSchema(BaseModel):
    track: TrackCreateSchema
    description: Optional[str] = None
    model_config = ConfigDict(str_strip_whitespace=True)


class SharedTrackResponseSchema(BaseModel):
    id: uuid.UUID
    sender_id: uuid.UUID
    description: Optional[str]
    created_at: str
    track: TrackSchema
    model_config = ConfigDict(from_attributes=True)
