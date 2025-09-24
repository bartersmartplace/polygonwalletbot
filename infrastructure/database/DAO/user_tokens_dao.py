from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .base_dao import BaseDAO
from ..model import UserTokens


class UserTokensDAO(BaseDAO[UserTokens]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserTokens)


    async def get_tokens_by_user(self, user_id: int) -> List[UserTokens]:
        result = await self.session.execute(select(self.model).filter_by(user_id=user_id))
        
        return result.scalars().all()


    async def user_has_token(self, user_id: int, token_id: int) -> bool:
        result = await self.session.execute(
            select(self.model)
            .filter_by(user_id=user_id, token_id=token_id)
        )

        return result.scalars().first() is not None