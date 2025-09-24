from typing import Tuple, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.dto import TokenDTO
from .base_dao import BaseDAO
from ..model import Pool


class PoolDAO(BaseDAO[Pool]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Pool)


    @staticmethod
    def __sort_tokens_by_symbol(token1: TokenDTO, token2: TokenDTO) -> Tuple[TokenDTO, TokenDTO]:
        return tuple(sorted([token1, token2], key=lambda token: token.symbol))
    

    async def get_by_token_pair(self, token1: TokenDTO, token2: TokenDTO) -> Optional[Pool]:
        first_token, second_token = self.__sort_tokens_by_symbol(token1, token2)
        
        result = await self.session.execute(
            select(self.model).where(
                (self.model.first_token_id == first_token.id) &
                (self.model.second_token_id == second_token.id)
            )
        )

        return result.scalars().first()


    async def set_token_pair(self, token1: TokenDTO, token2: TokenDTO, fee: int) -> Pool:        
        first_token, second_token = self.__sort_tokens_by_symbol(token1, token2)
        pool = await self.get_by_token_pair(first_token, second_token)

        if not pool:
            pool = Pool(
                first_token_id=first_token.address,
                second_token_id=second_token.address,
                fee=fee
            )
            self.session.add(pool)
            await self.session.commit()
            await self.session.refresh(pool)
        
        return pool