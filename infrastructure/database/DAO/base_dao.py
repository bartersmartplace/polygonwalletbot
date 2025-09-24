from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, TypeVar, Generic, List, Optional
from sqlalchemy.future import select


Model = TypeVar('Model')


class BaseDAO(Generic[Model]):
    def __init__(self, session: AsyncSession, model: Type[Model]):
        self.session = session
        self.model = model


    async def get_by_id(self, id: int) -> Optional[Model]:
        """Fetch a single record by its ID."""
        result = await self.session.get(self.model, id)
        return result


    async def get_all(self) -> List[Model]:
        """Fetch all records."""
        result = await self.session.execute(select(self.model))
        return result.scalars().all()


    async def create(self, **kwargs) -> Model:
        """Create a new record."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance


    async def update(self, id: int, **kwargs) -> Optional[Model]:
        """Update an existing record."""
        instance = await self.get_by_id(id)
        if not instance:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance


    async def delete(self, id: int) -> bool:
        """Delete a record by its ID."""
        instance = await self.get_by_id(id)
        if not instance:
            return False
        await self.session.delete(instance)
        await self.session.commit()
        return True