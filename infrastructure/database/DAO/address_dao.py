from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base_dao import BaseDAO
from ..model import Address


class AddressDAO(BaseDAO[Address]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Address)
    
    async def get_addresses_by_user(self, user_id: int) -> List[Address]:
        """Fetch all addresses associated with a specific user."""
        result = await self.session.execute(select(self.model).filter_by(user_id=user_id))

        return result.scalars().all()
    

    async def get_address_obj_by_address(self, address: str) -> Address:
        """Fetch all addresses associated with a specific user."""
        result = await self.session.execute(select(self.model).filter_by(address=address))

        return result.scalars().first()
