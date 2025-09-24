from typing import List, Optional
from ..DAO import DAOFactory
from infrastructure.database.model import Token
from app.application.dto import TokenDTO, UserDTO


class TokenRepository:
    def __init__(self, dao_factory: DAOFactory):
        self.__dao_factory = dao_factory


    async def get_token_by_id(self, token_id: int) -> Optional[TokenDTO]:
        """Fetch a token by its ID."""
        token = await self.__dao_factory.token_dao.get_by_id(token_id)
        if token:
            return token.dto
        
        return None


    async def get_token_by_network_name_and_symbol(self, network_name: str, symbol: str) -> Optional[TokenDTO]:
        """Fetch a token by network name and symbol using the DAO."""
        token = await self.__dao_factory.token_dao.get_token_by_network_name_and_symbol(network_name, symbol)
        if token:
            return token.dto
        
        return None


    async def get_all_tokens(self) -> List[TokenDTO]:
        """Fetch all tokens."""
        tokens = await self.__dao_factory.token_dao.get_all()

        return [token.dto for token in tokens if token]
    
    
    async def get_tokens_by_network(self, network_id: int) -> List[TokenDTO]:
        """Fetch tokens for a specific network."""
        tokens = await self.__dao_factory.token_dao.get_tokens_by_network(network_id)
        
        return [token.dto for token in tokens if token]
    

    async def get_user_tokens(self, user_id: int) -> List[TokenDTO]:
        tokens = await self.__dao_factory.user_tokens_dao.get_tokens_by_user(user_id)
        user_tokens: List[Token] = []
        for token in tokens:
            token_id = token.token_id
            token = await self.__dao_factory.token_dao.get_by_id(token_id)
            user_tokens.append(token)

        return [token.dto for token in user_tokens if token]


    async def get_stakeable_tokens(self) -> List[TokenDTO]:
        """Fetch tokens that can be staked."""
        stakeable_tokens = await self.__dao_factory.stake_dao.get_stake_tokens()

        return stakeable_tokens
        

    async def get_base_tokens(self) ->  List[TokenDTO]:
        """Fetch base tokens."""
        tokens = await self.__dao_factory.token_dao.get_base_tokens()

        return [token.dto for token in tokens if token]
    

    async def create_token(self, token_dto: TokenDTO) -> Optional[TokenDTO]:
        """Create and save a new token using TokenDTO."""
        created_token = await self.__dao_factory.token_dao.create(
            name=token_dto.name,
            symbol=token_dto.symbol,
            address=token_dto.address,
            standard=token_dto.standard,
            decimal=token_dto.decimal,
            network_id=token_dto.network_id,
            is_base=token_dto.is_base,
            last_checked_block=token_dto.last_checked_block
        )
        
        if created_token:
            return created_token.dto
        
        return None
    

    async def add_user_token(self, user: UserDTO, token: TokenDTO):
        added_token = await self.__dao_factory.user_tokens_dao.create(
            user_id=user.id,
            token_id=token.id
            )
        
        return added_token


    async def update_token(self, token_id: int, token_dto: TokenDTO) -> Optional[TokenDTO]:
        """Update an existing token using the provided TokenDTO."""
        token_data = {
            "name": token_dto.name,
            "symbol": token_dto.symbol,
            "address": token_dto.address,
            "standard": token_dto.standard,
            "decimal": token_dto.decimal,
            "network_id": token_dto.network_id,
            "is_base": token_dto.is_base,
            "last_checked_block": token_dto.last_checked_block,
        }
        token = await self.__dao_factory.token_dao.update(token_id, **token_data)

        if token:
            return token.dto

        return None


    async def is_stake_token(self, stake_token_id: int) -> bool:
        result = await self.__dao_factory.stake_dao.is_stake_token(stake_token_id)

        return result
    

    async def is_reward_token(self, reward_token_id: int) -> bool:
        result = await self.__dao_factory.stake_dao.is_reward_token(reward_token_id)

        return result