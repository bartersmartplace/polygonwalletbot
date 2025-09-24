from typing import List
from app.application.dto import AddressDTO, UserDTO
from app.application.service.common.error import AddressNotFoundError
from app.application.service.common.port import IRepositoryFactory
from app.application.service.model import Validator


class GetUserUseCase:
    def __init__(
            self,
            repository_factory: IRepositoryFactory
            ) -> None:
        self.__repository_factory = repository_factory


    async def get_all_users(
            self,
            ) -> List[UserDTO]:
        user_repository = self.__repository_factory.user_repository
        users = await user_repository.get_all_users()

        return users


    async def get_user_by_telegram_id(
            self,
            telegram_id: int
            ) -> UserDTO:
        self.__validate_input(telegram_id=telegram_id)
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)

        return user
    


    async def get_active_address_for_tg_user(
            self,
            telegram_id: int = None,
            tg_username: str = None
            ) -> AddressDTO:
        self.__validate_input(telegram_id=telegram_id)
        if telegram_id:
            self.__validate_input(telegram_id=telegram_id)
        user_repository = self.__repository_factory.user_repository
        if telegram_id:
            address = await user_repository.get_active_address_by_telegram_id(telegram_id)
            if not address:
                raise AddressNotFoundError(f"No active wallet address found for Telegram id: {telegram_id}")
        
        if tg_username:
            address = await user_repository.get_active_address_by_telegram_username(tg_username)
            if not address:
                raise AddressNotFoundError(f"No active wallet address found for Telegram username: @{tg_username}")

        return address


    async def get_language(
            self,
            telegram_id: int
            ) -> str:
        self.__validate_input(telegram_id=telegram_id)
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
        user_language = user.language if user else "en"
        language = user_language

        return language


    def __validate_input(self, telegram_id: int):
        telegram_id_field_name = "telegram_id"
        Validator.validate_number(telegram_id, telegram_id_field_name)
        Validator.is_more_than(telegram_id, 0, telegram_id_field_name)