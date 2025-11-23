import uuid
from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Reaction(Base):
    __tablename__ = "reactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    shared_track_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("shared_tracks.id"))
    emoji: Mapped[str] = mapped_column(String(50))
    user: Mapped["User"] = relationship("User", back_populates="reactions")
    shared_track: Mapped["SharedTrack"] = relationship(
        "SharedTrack", back_populates="reactions"
    )
