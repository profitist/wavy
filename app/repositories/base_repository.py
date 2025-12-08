from typing import Generic, TypeVar, Type, Optional, List, Any
import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import Base

model_type = TypeVar("model_type", bound=Base)


class BaseRepo(Generic[model_type]):
    def __init__(self, model: Type[model_type], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: uuid.UUID) -> Optional[model_type]:
        query = select(self.model).where(self.model.id == id)
        return await self.db.scalar(query)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[model_type]:
        query = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, attributes: dict[str, Any]) -> Optional[model_type]:
        obj = self.model(**attributes)
        self.db.add(obj)
        try:
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def update(
        self, id: uuid.UUID, attributes: dict[str, Any]
    ) -> Optional[model_type]:
        query = update(self.model).where(self.model.id == id).values(**attributes)
        try:
            result = await self.db.scalar(query)
            if result is None:
                return None
            await self.db.commit()
            return await self.get_by_id(id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e

    async def delete(self, id: uuid.UUID) -> bool:
        query = delete(self.model).where(self.model.id == id)
        try:
            result = await self.db.execute(query)
            await self.db.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e
