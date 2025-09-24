from typing import List
from app.application.dto import AddressDTO, UserDTO, ReferralDTO
from infrastructure.network.web3_adapter import Web3Adapter
from infrastructure.database import DAOFactory, RepositoryFactory
from app.application.use_case import (
    CreateUserUseCase,
    GetAddressListUseCase,
    UpdateUserUseCase,
    GetUserUseCase,
    GetReferralDataUseCase
)
from tg_bot.constants import NETWORK_RPC_URL


class UserController:
    def __init__(self, session, network_name: str = "Polygon"):
        self.__network_name = network_name
        self.__session = session


    async def create_user(
            self,
            telegram_id: int,
            tg_name: str = None,
            tg_username: str = None,
            referrer_id: int = None
            ):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        create_account_use_case = CreateUserUseCase(
            repository_factory=repository_factory,
        )
        return await create_account_use_case.create_user(
            telegram_id=telegram_id, tg_name=tg_name, tg_username=tg_username, referrer_id=referrer_id
        )


    async def get_user_by_telegram_id(self, telegram_id: int) -> UserDTO:
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        get_active_address_use_case = GetUserUseCase(repository_factory)
        user = await get_active_address_use_case.get_user_by_telegram_id(telegram_id=telegram_id)
        
        return user


    async def get_address_list(self, telegram_id: int) -> list[tuple]:
            repository_factory = RepositoryFactory(DAOFactory(self.__session))
            get_address_list_use_case = GetAddressListUseCase(repository_factory=repository_factory)
            addresses_list = await get_address_list_use_case.get_created_addresses_list(telegram_id=telegram_id)

            return addresses_list


    async def get_ref_data(self, telegram_id: int) -> ReferralDTO:
            repository_factory = RepositoryFactory(DAOFactory(self.__session))
            get_address_list_use_case = GetReferralDataUseCase(repository_factory=repository_factory)
            referral_data = await get_address_list_use_case.get_referral_data(telegram_id=telegram_id)

            return referral_data
    

    async def update_active_address(
              self,
              telegram_id: int,
              address,
              list_addresses: List[AddressDTO]
              ):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        update_address_user_case = UpdateUserUseCase(web3_adapter, repository_factory)
        await update_address_user_case.update_user_address(telegram_id, address, list_addresses)
        
        return address
    

    async def get_active_address(self, telegram_id):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        get_active_address_use_case = GetUserUseCase(repository_factory)
        active_address = await get_active_address_use_case.get_active_address_for_tg_user(telegram_id=telegram_id)
        
        return active_address
    

    async def update_language(
              self,
              telegram_id: int,
              language: str,
              ):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        update_address_user_case = UpdateUserUseCase(web3_adapter, repository_factory)
        language = await update_address_user_case.update_language(telegram_id, language)
        
        return language
    

    async def get_language(self, telegram_id):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        get_user_use_case = GetUserUseCase(repository_factory)
        language = await get_user_use_case.get_language(telegram_id=telegram_id)

        return language