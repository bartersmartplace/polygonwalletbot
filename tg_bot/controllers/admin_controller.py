from typing import List
from infrastructure.database import DAOFactory, RepositoryFactory
from app.application.dto import UserDTO
from app.application.use_case import (
    GetUserCountCase,
    GetUserUseCase
)

class AdminController:
    def __init__(self, session, network_name: str = "Polygon"):
        self.__session = session
        self.__network_name = network_name
    

    async def get_all_users(self) -> List[UserDTO]:
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        get_active_address_use_case = GetUserUseCase(repository_factory)
        users = await get_active_address_use_case.get_all_users()
        
        return users
    

    async def get_user_count(self):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        users_count_use_case = GetUserCountCase(repository_factory)
        users_count = await users_count_use_case.get_user_count()

        return users_count