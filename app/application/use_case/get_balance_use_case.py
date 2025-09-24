import asyncio
from domain.account.model import Account, AccountServiceFactory
from app.application.dto import AccountDTO, BalanceDTO
from app.application.service.common.error import AddressNotFoundError
from app.application.service.common.port import IRepositoryFactory, IAppWeb3Provider, IContractManager
from app.application.service.model import Token, Validator


class GetBalanceUseCase:
    def __init__(
            self,
            web3_adapter: IAppWeb3Provider,
            repository_factory: IRepositoryFactory,
            contract_manager: IContractManager
            ) -> None:
        self.__web3_adapter = web3_adapter
        self.__repository_factory = repository_factory
        self.__contract_manager = contract_manager


    async def get_account_balance_for_tg_user(self, telegram_id: int) -> BalanceDTO:
        self.__validate_input(telegram_id=telegram_id)

        user_repository = self.__repository_factory.user_repository
        token_repository = self.__repository_factory.token_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
        address = await user_repository.get_active_address_by_telegram_id(telegram_id)

        if address is None:
            raise AddressNotFoundError(f"No active wallet address found for Telegram id: {telegram_id}")
        
        account_data = AccountDTO(private_key=None, address=address.address)
        token_service = Token(self.__web3_adapter, self.__contract_manager)
        service_factory = AccountServiceFactory(token=token_service)
        account = Account(account_data, service_factory)
        base_tokens = await token_repository.get_base_tokens()
        user_tokens = await token_repository.get_user_tokens(user.id)

        seen = set()
        balances_tokens = []
        for token in base_tokens + user_tokens:
            key = (token.id, token.network_id, token.address)
            if key not in seen:
                seen.add(key)
                balances_tokens.append(token)

        get_balance_coroutines = [
            account.get_token_balance(token) for token in balances_tokens if token
        ]
        balances = await asyncio.gather(*get_balance_coroutines)
            
        tokens_with_balances = list(zip(balances_tokens, balances))

        return BalanceDTO(address.address, tokens_with_balances)


    async def get_token_balance_for_tg_user(self, telegram_id: int, network_name: str, symbol: str) -> BalanceDTO:
        self.__validate_input(telegram_id=telegram_id)
        user_repository = self.__repository_factory.user_repository
        token_repository = self.__repository_factory.token_repository
        address = await user_repository.get_active_address_by_telegram_id(telegram_id)
    
        if address is None:
            raise AddressNotFoundError(f"No active wallet address found for Telegram id: {telegram_id}")
        account_data = AccountDTO(private_key=None, address=address.address)
        token_service = Token(self.__web3_adapter, self.__contract_manager)
        service_factory = AccountServiceFactory(token=token_service)
        account = Account(account_data, service_factory)
        token = await token_repository.get_token_by_network_name_and_symbol(network_name=network_name, symbol=symbol)


        balance = await account.get_token_balance(token)
        token_balance_list = [(token, balance)]

        return BalanceDTO(address.address, token_balance_list)
    
        
    def __validate_input(self, telegram_id: int):
        telegram_id_field_name = "telegram_id"
        Validator.validate_number(telegram_id, telegram_id_field_name)
        Validator.is_more_than(telegram_id, 0, telegram_id_field_name)