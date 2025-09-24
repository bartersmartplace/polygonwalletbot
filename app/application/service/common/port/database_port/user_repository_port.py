from typing import Protocol
from typing import List, Optional
from app.application.dto import (
    AddressDTO,
    UserDTO
)


class IUserRepository(Protocol):
    async def get_all_users(self) -> List[UserDTO]:
        pass

    
    async def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        pass


    async def get_addresses_by_user(self, user_id: int) -> Optional[List[AddressDTO]]:
        pass


    async def get_user_by_telegram_id(self, tg_id: int) -> Optional[UserDTO]:
        pass


    async def add_user_address(self, user_id: int, address: str) -> AddressDTO:
        pass


    async def create_user(self, user: UserDTO) -> Optional[UserDTO]:
        pass


    async def update_user(self, user_id: int, user_dto: UserDTO) -> Optional[UserDTO]:
        pass


    async def get_referrals(self, user_id: int) -> List[UserDTO]:
        pass


    async def get_active_address_by_telegram_id(self, telegram_id: int) -> Optional[AddressDTO]:
        pass


    async def get_active_address_by_telegram_username(self, tg_username: str) -> Optional[AddressDTO]:
        pass


    async def get_user_count(self) -> int:
        pass


    async def user_has_token(self, user_id: int, token_id: int) -> bool:
        pass