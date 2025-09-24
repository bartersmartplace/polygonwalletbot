import asyncio
from domain.account.model import Account, AccountServiceFactory
from domain.common.errors import InsufficientFundsError
from app.application.dto import TradeDTO
from app.application.service.common.port import IAppWeb3Provider, IRepositoryFactory, IAppTradeProvider, IContractManager
from app.application.service.common.error import AddressDoesNotExistError, NotActiveAddressError
from app.application.service.model import Token, AppTrade, AppAccount, Validator
from app.config import SEED_PHRASE


class MakeTradeUseCase:
    def __init__(
            self,
            web3_adapter: IAppWeb3Provider,
            repository_factory: IRepositoryFactory,
            trade_service: IAppTradeProvider,
            contract_manager: IContractManager
        ) -> None:
        self.__web3_adapter = web3_adapter
        self.__repository_factory = repository_factory
        self.__trade_service = trade_service
        self.__contract_manager = contract_manager


    async def make_trade(
            self,
            telegram_id: int,
            password: str,
            trade_parameters_data: TradeDTO,
        ) -> str:
        await self.__validate_input(trade_parameters_data.amount_to_sell, telegram_id, password)
        account_data = AppAccount(self.__web3_adapter, password, telegram_id, SEED_PHRASE).get_account_dto()
        token_service = Token(self.__web3_adapter, self.__contract_manager)
        trade_service = AppTrade(self.__trade_service)
        service_factory = AccountServiceFactory(token=token_service, trade_provider=trade_service)
        account = Account(account_data, service_factory)
        token_balance = await account.get_token_balance(trade_parameters_data.sell_token)
        if token_balance < trade_parameters_data.amount_to_sell:
            raise InsufficientFundsError("Not enough funds")
        
        tx_hash = await account.trade(trade_parameters_data)

        return tx_hash
    

    async def __validate_input(self, amount_to_sell: int, telegram_id: int,  password: str):
        amount_to_sell_field_name = "amount to sell"
        Validator.validate_number(amount_to_sell, amount_to_sell_field_name)
        Validator.is_more_than(amount_to_sell, 0, amount_to_sell_field_name)
        telegram_id_field_name = "telegram_id"
        Validator.validate_number(telegram_id, telegram_id_field_name)
        Validator.is_more_than(telegram_id, 0, telegram_id_field_name)
        Validator.validate_password(password)
        user_repository = self.__repository_factory.user_repository

        user = await user_repository.get_user_by_telegram_id(telegram_id)
        active_address,  user_addresses = await asyncio.gather(
        user_repository.get_active_address_by_telegram_id(telegram_id),
        user_repository.get_addresses_by_user(user.id)
        )

        account_data = AppAccount(
            self.__web3_adapter, password, telegram_id, SEED_PHRASE
        ).get_account_dto()
        
        if not Validator.is_address_exist(account_data.address, user_addresses):
            raise AddressDoesNotExistError("You don't have an address with that password")

        if account_data.address != active_address.address:
            raise NotActiveAddressError("You are using an address from another wallet")