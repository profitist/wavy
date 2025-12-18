import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, func, ForeignKey, Table, Column, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from app.models.friendship_status import FriendshipStatus


# app/models/friendship.py
import uuid
from sqlalchemy import Table, Column, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.models.friendship_status import FriendshipStatus

Friendship = Table(
    "friendship",  # имя таблицы
    Base.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column("sender_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column("receiver_id", UUID(as_uuid=True), ForeignKey("users.id"), nullable=False),
    Column(
        "status",
        SQLEnum(FriendshipStatus, name="friendship_status_enum"),
        default=FriendshipStatus.PENDING,
        nullable=False,
    ),
)
