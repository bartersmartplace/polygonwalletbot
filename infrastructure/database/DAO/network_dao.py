from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base_dao import BaseDAO
from ..model import Network


class NetworkDAO(BaseDAO[Network]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Network)
    

    async def get_network_by_network_id(self, network_id: str) -> Optional[Network]:
        """Fetch a network by its network_id."""
        result = await self.session.execute(select(self.model).filter_by(network_id=network_id))
        return result.scalars().first()
    

    async def get_network_by_network_name(self, name: str) -> Optional[Network]:
        """Fetch a network by its name."""
        result = await self.session.execute(
            select(self.model).filter_by(name=name)
        )
        return result.scalars().first()