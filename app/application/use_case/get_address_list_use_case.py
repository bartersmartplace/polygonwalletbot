from typing import List
from app.application.dto import AddressDTO
from app.application.service.common.port import IRepositoryFactory


class GetAddressListUseCase:
    def __init__(
            self,
            repository_factory: IRepositoryFactory,
            ) -> None:
        self.__repository_factory = repository_factory


    async def get_created_addresses_list(self, telegram_id: int) -> List[AddressDTO]:
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
        if not user:
            return None
        address_list = await user_repository.get_addresses_by_user(user.id)
        
        return address_list