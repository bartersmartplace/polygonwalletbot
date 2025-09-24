from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from .base_dao import BaseDAO
from ..model import Stake, Token
from app.application.dto import TokenDTO


class StakeDAO(BaseDAO[Stake]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Stake)


    async def is_stake_token(self, stake_token_id: int) -> bool:
        """Check if the token can be staked."""
        result = await self.session.execute(
            select(self.model).filter_by(stake_token_id=stake_token_id)
        )

        return result.scalars().first() is not None


    async def is_reward_token(self, reward_token_id: int) -> bool:
        """Check if the token can be a staking reward."""
        result = await self.session.execute(
            select(self.model).filter_by(reward_token_id=reward_token_id)
        )

        return result.scalars().first() is not None
    

    async def get_stake_tokens(self) -> List[TokenDTO]:
        """Fetch all tokens used as stake tokens and return them as TokenDTOs."""
        result = await self.session.execute(
            select(Token)
            .join(Stake, Stake.stake_token_id == Token.id)
        )
        tokens = result.scalars().all()

        return [token.dto for token in tokens]