import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.reactions import Reaction
from app.repositories.base_repository import BaseRepo


class ReactionRepository(BaseRepo[Reaction]):
    def __init__(self, db: AsyncSession):
        super().__init__(Reaction, db)

    async def get_by_user_and_share(
        self, user_id: uuid.UUID, share_id: uuid.UUID
    ) -> Optional[Reaction]:
        query = select(self.model).where(
            (self.model.user_id == user_id) & (self.model.shared_track_id == share_id)
        )
        return await self.db.scalar(query)

    async def get_for_share(self, share_id: uuid.UUID) -> List[Reaction]:
        query = (
            select(self.model)
            .where(self.model.shared_track_id == share_id)
            .options(selectinload(self.model.user))
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())
