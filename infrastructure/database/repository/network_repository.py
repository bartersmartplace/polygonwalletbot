from typing import List, Optional
from ..DAO import DAOFactory
from ..model import Network


class NetworkRepository:
    def __init__(self, dao_factory: DAOFactory):
        self.__dao_factory = dao_factory

    async def get_network_by_id(self, id: int) -> Optional[Network]:
        """Fetch a network by its ID."""
        return await self.__dao_factory.network_dao.get_by_id(id)
            

    async def get_network_by_name(self, name: str) -> Optional[Network]:
        """Fetch a network by its name."""
        return await self.__dao_factory.network_dao.get_network_by_network_name(name)


    async def get_all_networks(self) -> List[Network]:
        """Fetch all networks."""
        return await self.__dao_factory.network_dao.get_all()


    async def create_network(self, **network_data) -> Network:
        """Create and save a new network."""
        return await self.__dao_factory.network_dao.create(**network_data)


    async def update_network(self, network_id: int, **network_data) -> Optional[Network]:
        """Update an existing network."""
        return await self.__dao_factory.network_dao.update(network_id, **network_data)


    async def delete_network(self, network_id: int) -> bool:
        """Delete a network by its ID."""
        return await self.__dao_factory.network_dao.delete(network_id)