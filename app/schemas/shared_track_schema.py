from datetime import datetime
import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.track_schema import TrackCreateSchema, TrackSchema
from app.schemas.user_schema import UserInFeedSchema

class ShareRequestSchema(BaseModel):
    track: TrackCreateSchema
    description: Optional[str] = None
    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)


class SharedTrackResponseSchema(BaseModel):
    id: uuid.UUID
    sender_id: UserInFeedSchema
    description: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)
    track: TrackSchema
    model_config = ConfigDict(from_attributes=True)
