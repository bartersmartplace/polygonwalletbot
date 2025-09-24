from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from .base_dao import BaseDAO
from ..model import User, Address
from sqlalchemy import func


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
    
    
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Fetch a user by their Telegram ID."""
        result = await self.session.execute(select(self.model).filter_by(tg_id=telegram_id))

        return result.scalars().first()
    

    async def get_referrals(self, user_id: int) -> List[User]:
        """Fetch all users referred by a specific user."""
        result = await self.session.execute(select(self.model).filter_by(referrer_id=user_id))

        return result.scalars().all()


    async def get_active_address_by_telegram_id(self, telegram_id: int) -> Optional[Address]:
        """Fetch the active address for a specific user."""
        result = await self.session.execute(
            select(User)
            .options(joinedload(User.active_address))
            .filter(User.tg_id == telegram_id)
        )
        user = result.scalars().first()
        if user:
            return user.active_address
        return None


    async def get_active_address_by_telegram_username(self, tg_username: str) -> Optional[Address]:
        """Fetch the active address for a specific user."""
        result = await self.session.execute(
        select(User)
        .options(joinedload(User.active_address))
        .filter(User.tg_username == tg_username)
        )
        user = result.scalars().first()
        return user.active_address if user else None
    

    async def get_user_count(self) -> int:
        """Get the total count of users."""
        result = await self.session.execute(select(func.count(self.model.id)))
        return result.scalar()