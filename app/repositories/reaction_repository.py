import uuid
from typing import Optional, List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.reactions import Reaction

class Repository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_reaction(self, reaction: Reaction) -> Reaction:
        self.db.add(reaction)
        await self.db.commit()
        await self.db.refresh(reaction)
        return reaction

    async def get_by_user_and_share(self, user_id: uuid.UUID, share_id: uuid.UUID) -> Optional[Reaction]:
        query = select(Reaction).where((Reaction.user_id == user_id) &
                                       (Reaction.shared_track_id == share_id))
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_reactions_for_share(self, share_id: uuid.UUID) -> List[Reaction]:
        query = select(Reaction)\
            .where(Reaction.shared_track_id == share_id)\
            .options(selectinload(Reaction.user)) # Подгрузить, КТО поставил
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def remove_reaction(self, reaction_id: uuid.UUID) -> bool:
        query = delete(Reaction).where(Reaction.id == reaction_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0
