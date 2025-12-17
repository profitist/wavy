"""add musicplatform enum and platform column

Revision ID: 647b8bb3d005
Revises: 8a9a93dbcf23
Create Date: 2025-12-12 23:39:38.839183
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "647b8bb3d005"
down_revision: Union[str, Sequence[str], None] = "8a9a93dbcf23"
branch_labels = None
depends_on = None

# Объявляем ENUM ТОЛЬКО здесь
music_platform = sa.Enum(
    "SPOTIFY", "YANDEX", "APPLE", "VK", "OTHER", name="musicplatform"
)


def upgrade() -> None:
    bind = op.get_bind()

    # 1. Создаём enum type
    music_platform.create(bind, checkfirst=True)

    # 2. Добавляем колонку с ВРЕМЕННЫМ default
    op.add_column(
        "tracks",
        sa.Column("platform", music_platform, nullable=False, server_default="OTHER"),
    )

    # 3. Убираем default
    op.alter_column("tracks", "platform", server_default=None)


def downgrade() -> None:
    bind = op.get_bind()

    # Удаляем колонку
    op.drop_column("tracks", "platform")

    # Удаляем enum type
    music_platform.drop(bind, checkfirst=True)
