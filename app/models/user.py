import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.friendship import Friendship

class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(250), index=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    profile_picture_url: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    shared_tracks: Mapped[List["SharedTrack"]] = relationship("SharedTrack", back_populates="sender")
    reactions: Mapped[List["Reaction"]] = relationship("Reaction", back_populates="user")

    friends: Mapped[List["User"]] = relationship("User", back_populates="friends")