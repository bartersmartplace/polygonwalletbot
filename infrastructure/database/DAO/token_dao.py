from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from .base_dao import BaseDAO
from ..model import Token, Stake


class TokenDAO(BaseDAO[Token]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Token)


    async def get_tokens_by_network(self, network_id: int) -> List[Token]:
        """Fetch tokens for a specific network."""
        result = await self.session.execute(select(self.model).filter_by(network_id=network_id))

        return result.scalars().all()


    async def get_base_tokens(self) -> List[Token]:
        """Fetch tokens that can be staked."""
        result = await self.session.execute(select(self.model).filter_by(is_base=True))

        return result.scalars().all()


    async def get_token_by_network_name_and_symbol(self, network_name: str, symbol: str) -> Optional[Token]:
        """Fetch a token by network name and symbol."""
        result = await self.session.execute(
            select(Token)
            .join(Token.network)
            .options(joinedload(Token.network))
            .filter(Token.network.has(name=network_name), Token.symbol == symbol)
        )

        return result.scalars().first()