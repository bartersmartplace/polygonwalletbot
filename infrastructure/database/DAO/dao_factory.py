from sqlalchemy.ext.asyncio import AsyncSession
from .address_dao import AddressDAO
from .network_dao import NetworkDAO
from .pool_dao import PoolDAO
from .token_dao import TokenDAO
from .user_dao import UserDAO
from .user_tokens_dao import UserTokensDAO
from .stake_dao import StakeDAO


class DAOFactory:
    def __init__(self, session: AsyncSession):
        self.session = session


    @property
    def address_dao(self):
        """Return AddressDAO instance."""
        return AddressDAO(self.session)


    @property
    def network_dao(self):
        """Return NetworkDAO instance."""
        return NetworkDAO(self.session)


    @property
    def pool_dao(self):
        """Return PoolDAO instance."""
        return PoolDAO(self.session)


    @property
    def token_dao(self):
        """Return TokenDAO instance."""
        return TokenDAO(self.session)


    @property
    def user_dao(self):
        """Return UserDAO instance."""
        return UserDAO(self.session)


    @property
    def user_tokens_dao(self):
        """Return UserTokensDAO instance."""
        return UserTokensDAO(self.session)
    
    
    @property
    def stake_dao(self):
        """Return StakeDAO instance"""
        return StakeDAO(self.session)