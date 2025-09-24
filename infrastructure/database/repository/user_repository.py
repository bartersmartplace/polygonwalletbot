import asyncio
from typing import List, Optional
from ..DAO import DAOFactory
from ..model import Address
from app.application.dto import UserDTO, AddressDTO, TokenDTO


class UserRepository:
    def __init__(self, dao_factory: DAOFactory):
        self.__dao_factory = dao_factory


    async def get_all_users(self) -> List[UserDTO]:
        users = await self.__dao_factory.user_dao.get_all()
        users_dto = [user.dto for user in users]
        return users_dto


    async def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        """Fetch a user by ID."""
        user = await self.__dao_factory.user_dao.get_by_id(user_id)
        if user:
            return user.dto
        
        return None


    async def get_user_by_telegram_id(self, tg_id: int) -> Optional[UserDTO]:
        """Fetch a user by their Telegram ID."""
        user = await self.__dao_factory.user_dao.get_by_telegram_id(tg_id)
        if user:
            return user.dto


    async def get_addresses_by_user(self, user_id: int) -> List[AddressDTO]:
        """Fetch all addresses associated with a specific user."""
        addresses =  await self.__dao_factory.address_dao.get_addresses_by_user(user_id)

        return [address.dto for address in addresses if address]


    async def get_tokens_by_user_id(self, user_id: int) -> List[TokenDTO]:
        """Get all tokens associated with a specific user."""
        user_tokens = await self.__dao_factory.user_tokens_dao.get_tokens_by_user(user_id)
        
        token_coroutines = [
            self.__dao_factory.token_dao.get_by_id(user_token.token_id) 
            for user_token in user_tokens
        ]
        tokens = await asyncio.gather(*token_coroutines)
        
        return [token.dto for token in tokens if token]


    async def get_active_address_by_telegram_id(self, telegram_id: int) -> Optional[AddressDTO]:
        address = await self.__dao_factory.user_dao.get_active_address_by_telegram_id(telegram_id)
        if address:
            return address.dto
        
        return None


    async def get_active_address_by_telegram_username(self, tg_username: str) -> Optional[AddressDTO]:
        address = await self.__dao_factory.user_dao.get_active_address_by_telegram_username(tg_username)
        if address:
            return address.dto
        
        return None


    async def get_referrals(self, user_id: int) -> List[UserDTO]:
        """Fetch all users referred by a specific user."""
        users = await self.__dao_factory.user_dao.get_referrals(user_id)

        return [user.dto for user in users if user]


    async def create_user(self, user_dto: UserDTO) -> Optional[UserDTO]:
        """Create and save a new user using UserDTO."""
        created_user = await self.__dao_factory.user_dao.create(
            tg_id=user_dto.tg_id,
            tg_name=user_dto.tg_name,
            tg_username=user_dto.tg_username,
            address_limit=user_dto.address_limit,
            language=user_dto.language,
            is_admin=user_dto.is_admin,
            is_banned=user_dto.is_banned,
            referrer_id=user_dto.referrer_id
        )
        if created_user:
            return created_user.dto

        return None
    

    async def update_user(self, user_id: int, user_dto: UserDTO) -> Optional[UserDTO]:
        """Update an existing user using the provided UserDTO."""
        user_data = {
            "tg_id": user_dto.tg_id,
            "tg_name": user_dto.tg_name,
            "tg_username": user_dto.tg_username,
            "active_address_id": user_dto.active_address_id,
            "address_limit": user_dto.address_limit,
            "language": user_dto.language,
            "is_admin": user_dto.is_admin,
            "is_banned": user_dto.is_banned,
            "referrer_id": user_dto.referrer_id,
            "tokens_limit": user_dto.tokens_limit
        }
        user = await self.__dao_factory.user_dao.update(user_id, **user_data)
        
        if user:
            return user.dto
        
        return None



    async def add_user_address(self, user_id: int, address: str) -> AddressDTO:
        address_data = {
            "address": address,
            "user_id": user_id,
        }
        address_data["user_id"] = user_id
        new_address: Address = await self.__dao_factory.address_dao.create(**address_data)
        
        user = await self.__dao_factory.user_dao.get_by_id(user_id)
        if user:
            user.active_address_id = new_address.id
            await self.update_user(user_id, user.dto)

        return new_address.dto


    async def get_user_count(self) -> int:
        user_count = await self.__dao_factory.user_dao.get_user_count()
        
        return user_count
    

    async def user_has_token(self, user_id: int, token_id: int) -> bool:
        result = await self.__dao_factory.user_tokens_dao.user_has_token(user_id, token_id)
        
        return result