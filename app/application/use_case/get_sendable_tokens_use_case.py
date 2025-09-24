import asyncio
from typing import List
from app.application.dto import TokenDTO
from app.application.service.common.port import IRepositoryFactory


class GetTokensUseCase:
    def __init__(
            self,
            repository_factory: IRepositoryFactory,
            ) -> None:
        self.__repository_factory = repository_factory


    async def get_sendable_tokens(self, telegram_id: int) -> List[TokenDTO]:
        token_repository = self.__repository_factory.token_repository
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
        base_tokens = await token_repository.get_base_tokens()
        user_tokens = await token_repository.get_user_tokens(user.id)
        seen = set()
        balances_tokens = []
        for token in base_tokens + user_tokens:
            key = (token.id, token.network_id, token.address)
            if key not in seen:
                seen.add(key)
                balances_tokens.append(token)

        tasks = [token_repository.is_reward_token(token.id) for token in balances_tokens]
        results = await asyncio.gather(*tasks)
        sendable_tokens = [
            token for token, is_reward in zip(balances_tokens, results) if not is_reward
        ]
        
        return sendable_tokens
    
    
    async def get_user_tokens(self, telegram_id: int) -> List[TokenDTO]:
        token_repository = self.__repository_factory.token_repository
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
        user_tokens = await token_repository.get_user_tokens(user.id)

        return user_tokens