import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base


class SharedTrack(Base):
    __tablename__ = "shared_tracks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    track_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tracks.id"))
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    sender: Mapped["User"] = relationship("User", back_populates="shared_tracks")
    track: Mapped["Track"] = relationship("Track", back_populates="shares")
    reactions: Mapped[List["Reaction"]] = relationship(
        "Reaction", back_populates="shared_track"
    )