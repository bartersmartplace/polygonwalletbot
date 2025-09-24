import asyncio
from typing import Tuple
from domain.account.model import Account, AccountServiceFactory
from app.application.service.common.port import IRepositoryFactory, IAppWeb3Provider, IContractManager
from app.application.service.common.error import AddressNotFoundError, TokenNotSupportedError, TokenNotFoundError, AddressDoesNotExistError, NotActiveAddressError
from app.application.service.model import Token, AppAccount, Validator
from app.config import SEED_PHRASE


class SendTokenUseCase:
    def __init__(
        self,
        web3_adapter: IAppWeb3Provider,
        repository_factory: IRepositoryFactory,
        contract_manager: IContractManager,
    ) -> None:
        self.__web3_adapter = web3_adapter
        self.__repository_factory = repository_factory
        self.__contract_manager = contract_manager


    async def send_tokens_to_external_address(
        self,
        telegram_id: int,
        password: str,
        network_name: str,
        token_symbol: str,
        amount: float,
        to_address: str,
    ) -> str:
        account, send_token, adjusted_amount = await self.__prepare_transaction(
            telegram_id, password, network_name, token_symbol, amount
        )
        to_address =Validator.is_correct_address(self.__web3_adapter, to_address)

        tx_hash = await account.send_tokens(adjusted_amount, to_address, send_token)

        return tx_hash


    async def send_tokens_to_username(
        self,
        telegram_id: int,
        password: str,
        network_name: str,
        token_symbol: str,
        amount: float,
        recipient_username: str,
    ) -> str:
        account, send_token, adjusted_amount = await self.__prepare_transaction(
            telegram_id, password, network_name, token_symbol, amount
        )
        recipient_address_dto = await self.__repository_factory.user_repository.get_active_address_by_telegram_username(
            recipient_username
        )
        if not recipient_address_dto:
            raise AddressNotFoundError(
                f"No active wallet address found for Telegram username: {recipient_username}"
            )
        recipient_address_dto.address = Validator.is_correct_address(self.__web3_adapter, recipient_address_dto.address)

        tx_hash = await account.send_tokens(adjusted_amount, recipient_address_dto.address, send_token)

        return tx_hash


    async def __prepare_transaction(
        self, telegram_id: int, password: str, network_name: str, token_symbol: str, amount: float
    ) -> Tuple[Account, Token, int]:
        """Prepare the sender account and validate the token."""
        await self.__validate_input(telegram_id=telegram_id, password=password, amount=amount)
        amount = float(amount)
        account_data = AppAccount(
            self.__web3_adapter, password, telegram_id, SEED_PHRASE
        ).get_account_dto()
        token_service = Token(self.__web3_adapter, self.__contract_manager)
        service_factory = AccountServiceFactory(token=token_service)
        account = Account(account_data, service_factory)

        token_repository = self.__repository_factory.token_repository
        send_token = await token_repository.get_token_by_network_name_and_symbol(network_name, token_symbol)
        if not send_token:
            raise TokenNotFoundError(
                f"Token not found for network: {network_name}, symbol: {token_symbol}"
            )
        is_reward = await token_repository.is_reward_token(send_token.id)
        if is_reward:
            raise TokenNotSupportedError(
                f"The {send_token.symbol} sending operation is not supported"
            )

        adjusted_amount = int(amount * 10**send_token.decimal)

        return account, send_token, adjusted_amount


    async def __validate_input(self, telegram_id: int, password: str, amount: int):
        """Validate common input fields."""
        amount_field_name = "amount to send"
        Validator.validate_number(amount, amount_field_name)
        Validator.is_more_than(amount, 0, amount_field_name)

        telegram_id_field_name = "telegram id"
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