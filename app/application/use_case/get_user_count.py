from app.application.dto import AddressDTO
from app.application.service.common.error import AddressNotFoundError
from app.application.service.common.port import IRepositoryFactory
from app.application.service.model import Validator


class GetUserCountCase:
    def __init__(
            self,
            repository_factory: IRepositoryFactory
            ) -> None:
        self.__repository_factory = repository_factory
    

    async def get_user_count(self):
        user_repository = self.__repository_factory.user_repository
        user_count = await user_repository.get_user_count()
        
        return user_count