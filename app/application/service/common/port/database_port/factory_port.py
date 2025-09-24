from typing import Protocol
from .user_repository_port import IUserRepository
from .token_repository_port import ITokenRepository

class IRepositoryFactory(Protocol):
    """Interface for RepositoryFactory, defining the expected repository properties."""
    @property
    def user_repository(self) -> IUserRepository:
        """Return an instance of UserRepository."""
        pass

    @property
    def token_repository(self) -> ITokenRepository:
        """Return an instance of TokenRepository."""
        pass