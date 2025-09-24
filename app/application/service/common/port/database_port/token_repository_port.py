from typing import Protocol, Optional, List
from app.application.dto import UserDTO, TokenDTO


class ITokenRepository(Protocol):
    async def get_token_by_network_name_and_symbol(self, network_name: str, symbol: str) -> Optional[TokenDTO]:
        pass


    async def get_base_tokens(self) -> List[TokenDTO]:
        pass

    
    async def is_reward_token(self, reward_token_id: int) -> bool:
        pass


    async def get_user_tokens(self, user_id: int) -> List[TokenDTO]:
        pass


    async def create_token(self, token_dto: TokenDTO) -> Optional[TokenDTO]:
        pass


    async def add_user_token(self, user: UserDTO, token: TokenDTO):
        pass
    

    async def update_token(self, token_id: int, token_dto: TokenDTO) -> Optional[TokenDTO]:
        pass