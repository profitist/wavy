import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, func, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.friendship import Friendship


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(250), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=True)
    role: Mapped[str] = mapped_column(String(15), default="user", nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(12), nullable=True)
    user_picture_number: Mapped[int] = mapped_column(Integer, default=1)
    profile_picture_url: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    shared_tracks: Mapped[List["SharedTrack"]] = relationship(
        "SharedTrack", back_populates="sender"
    )
    reactions: Mapped[List["Reaction"]] = relationship(
        "Reaction", back_populates="user"
    )
    friends: Mapped[list["User"]] = relationship(
        "User",
        secondary=Friendship,
        primaryjoin=lambda: Friendship.c.sender_id == User.id,
        secondaryjoin=lambda: Friendship.c.receiver_id == User.id,
        backref="friend_of",
    )
