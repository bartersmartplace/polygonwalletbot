import asyncio
from typing import List
from app.application.dto import AddressDTO
from app.application.service.common.port import IAppWeb3Provider, IRepositoryFactory
from app.application.service.common.error import AddressAlreadyExists, NotActiveAddressError
from app.application.service.model import Validator, AppAccount
from app.config import SEED_PHRASE


class ValidatePasswordUseCase:
    def __init__(
            self,
            web3_adapter: IAppWeb3Provider,
            repository_factory: IRepositoryFactory,
        ) -> None:
        self.__web3_adapter = web3_adapter
        self.__repository_factory = repository_factory


    async def validate_password(
            self,
            telegram_id: int,
            password: str
            ) -> bool:
        Validator.validate_password(password)
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
        addresses = await asyncio.gather(
        user_repository.get_active_address_by_telegram_id(telegram_id),
        user_repository.get_addresses_by_user(user.id)
        )
        account_data = AppAccount(
            self.__web3_adapter, password, telegram_id, SEED_PHRASE
        ).get_account_dto()
        active_address: AddressDTO = addresses[0]
        user_addresses: List[AddressDTO] = addresses[1]
        
        if Validator.is_address_exist(account_data.address, user_addresses):
            AddressAlreadyExists("You don't have an address with that password")
        
        if account_data != active_address.address:
            return NotActiveAddressError("You are using an address from another wallet")

        return True