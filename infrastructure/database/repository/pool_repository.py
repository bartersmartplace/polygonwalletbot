from typing import Optional
from app.application.dto import TokenDTO
from ..model import Pool
from ..DAO import DAOFactory


class PoolRepository:
    def __init__(
            self,
            dao_factory: DAOFactory
            ):
        self.__pool_dao = dao_factory.pool_dao

    async def find_pool_by_tokens(self, token1: TokenDTO, token2: TokenDTO) -> Optional[Pool]:
        """
        Find a pool by token pair if it exists
        """
        return await self.__pool_dao.get_by_token_pair(token1, token2)

    async def create_or_get_pool(self, token1: TokenDTO, token2: TokenDTO, fee: int) -> Pool:
        """
        Create a new pool for the token pair if it doesn't exist, or return existing pool
        """
        return await self.__pool_dao.set_token_pair(token1, token2, fee)

    async def get_pool_by_id(self, pool_id: int) -> Optional[Pool]:
        """
        Get pool by its ID
        """
        return await self.__pool_dao.get_by_id(pool_id)

    async def get_all_pools(self) -> list[Pool]:
        """
        Get all existing pools
        """
        return await self.__pool_dao.get_all()