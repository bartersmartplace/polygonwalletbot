from typing import List
from app.application.dto import AddressDTO
from app.application.service.common.error import AddressNotFoundError
from app.application.service.common.port import IAppWeb3Provider, IRepositoryFactory
from app.application.service.model import Validator


class UpdateUserUseCase:
    def __init__(
            self,
            web3_adapter: IAppWeb3Provider,
            repository_factory: IRepositoryFactory,
        ) -> None:
        self.__web3_adapter = web3_adapter
        self.__repository_factory = repository_factory


    async def update_user_address(
           self,
           telegram_id,
           address: str,
           addresses_list: List[AddressDTO]
           ) -> str:
        
        address = Validator.is_correct_address(self.__web3_adapter, address)
        address_data = Validator.is_address_exist(address, addresses_list)
        if not address_data:
            raise AddressNotFoundError("There is no such address")
        
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
        user.active_address_id = address_data.id
        await user_repository.update_user(user_id=user.id, user_dto=user)

        return address
    

    async def update_language(
           self,
           telegram_id,
           language: str,
           ) -> str:
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
        user.language = language
        await user_repository.update_user(user_id=user.id, user_dto=user)

        return language