import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, func, ForeignKey, Table, Column, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from friendship_status import FriendshipStatus


friendship = Table(
    "friendship",
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("from_user_id", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("status", Enum(FriendshipStatus), ForeignKey("status.id"), nullable=False)
)
