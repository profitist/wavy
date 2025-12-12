"""fixxxx

Revision ID: 67b0e3b16a9a
Revises:
Create Date: 2025-12-06 22:39:06.657248
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "67b0e3b16a9a"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ---------- UPGRADE ----------

def upgrade() -> None:
    # ---------- ENUMS (safe creation) ----------
    op.execute("CREATE TYPE musicplatform AS ENUM ('SPOTIFY', 'YANDEX', 'APPLE', 'VK', 'OTHER')")
    op.execute("CREATE TYPE friendship_status_enum AS ENUM ('PENDING', 'ACCEPTED', 'REJECTED')")

    # ---------- TABLES ----------

    op.create_table(
        "tracks",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("author", sa.String(), nullable=False),
        sa.Column("album_cover_url", sa.String(), nullable=True),
        sa.Column("platform", sa.Enum(name="musicplatform"), nullable=False),
        sa.Column("external_link", sa.String(), nullable=False),
    )

    op.create_index("ix_tracks_author", "tracks", ["author"])
    op.create_index("ix_tracks_title", "tracks", ["title"])

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("username", sa.String(length=40), nullable=False),
        sa.Column("description", sa.String(length=250)),
        sa.Column("hashed_password", sa.String(length=50)),
        sa.Column("role", sa.String(length=15)),
        sa.Column("phone_number", sa.String(length=12)),
        sa.Column("profile_picture_url", sa.String(length=100)),
        sa.Column("created_at", sa.DateTime()),
    )

    op.create_index("ix_users_username", "users", ["username"], unique=True)

    op.create_table(
        "friendship",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("sender_id", sa.UUID(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("receiver_id", sa.UUID(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.Enum(name="friendship_status_enum"), nullable=False),
    )

    op.create_table(
        "shared_tracks",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("sender_id", sa.UUID(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("track_id", sa.UUID(), sa.ForeignKey("tracks.id"), nullable=False),
        sa.Column("description", sa.String()),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
    )

    op.create_table(
        "reactions",
        sa.Column("id", sa.UUID(), primary_key=True),
        sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("shared_track_id", sa.UUID(), sa.ForeignKey("shared_tracks.id"), nullable=False),
        sa.Column("emoji", sa.String(length=50), nullable=False),
    )


# ---------- DOWNGRADE ----------

def downgrade() -> None:
    op.drop_table("reactions")
    op.drop_table("shared_tracks")
    op.drop_table("friendship")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_tracks_title", table_name="tracks")
    op.drop_index("ix_tracks_author", table_name="tracks")
    op.drop_table("tracks")

    # Remove ENUMs (safe)
    op.execute("DROP TYPE IF EXISTS musicplatform")
    op.execute("DROP TYPE IF EXISTS friendship_status_enum")
