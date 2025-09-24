from ..DAO import DAOFactory 
from .pool_repository import PoolRepository
from .user_repository import UserRepository
from .token_repository import TokenRepository
from .network_repository import NetworkRepository
from .address_repository import AddressRepository


class RepositoryFactory:
    def __init__(self, dao_factory: DAOFactory):
        self.__dao_factory = dao_factory


    @property
    def pool_repository(self) -> PoolRepository:
        """Return an instance of PoolRepository."""
        return PoolRepository(self.__dao_factory)
    
    
    @property
    def user_repository(self) -> UserRepository:
        """Return an instance of UserRepository"""
        return UserRepository(self.__dao_factory)
    

    @property
    def token_repository(self) -> TokenRepository:
        """Return an instance of UserRepository"""
        return TokenRepository(self.__dao_factory)
    

    @property
    def network_repository(self) -> NetworkRepository:
        """Return an instance of NetworkRepository"""
        return NetworkRepository(self.__dao_factory)
    

    @property
    def address_repository(self) -> AddressRepository:
        return AddressRepository(self.__dao_factory)