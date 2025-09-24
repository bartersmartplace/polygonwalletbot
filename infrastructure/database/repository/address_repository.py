from typing import List, Optional
from ..DAO import DAOFactory
from ..model import Address


class AddressRepository:
    def __init__(self, dao_factory: DAOFactory):
        self.__dao_factory = dao_factory


    async def get_all_addresses(self):
        return await self.__dao_factory.address_dao.get_all()
    

    async def get_user_address_obj(self, address: str):
        return await self.__dao_factory.address_dao.get_address_obj_by_address(address)