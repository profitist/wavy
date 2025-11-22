import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Friendship(Base):
    __tablename__ = "friendship"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, default=uuid.uuid4)
    receiver_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True, default=uuid.uuid4)
    sender: Mapped["User"] = relationship("User", foreign_keys=[sender_id])
    receiver: Mapped["User"] = relationship("User", foreign_keys=[receiver_id])

    