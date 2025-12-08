import uuid
from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.music_platform import MusicPlatform


class Track(Base):
    __tablename__ = "tracks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String, index=True)
    author: Mapped[str] = mapped_column(String, index=True)
    album_cover_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    platform: Mapped[MusicPlatform] = mapped_column(default=MusicPlatform.OTHER)
    external_link: Mapped[str] = mapped_column(String)
    shares: Mapped[List["SharedTrack"]] = relationship(
        "SharedTrack", back_populates="track"
    )
