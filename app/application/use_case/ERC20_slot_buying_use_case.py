import asyncio
from domain.account.model import Account, AccountServiceFactory
from app.application.dto import TokenDTO
from app.application.service.common.port import IRepositoryFactory, IAppWeb3Provider, IContractManager
from app.application.service.common.error import AddressAlreadyExists, NotActiveAddressError, TokenAlreadyBeenAddedError
from app.application.service.model import AppAccount, Token, Validator
from app.config import (
    SEED_PHRASE,
    REFERRER_PART_TO_ADD_ERC20,
    RECIPIENT,
    REFERRER_PART_TO_ADD_ERC20_TO_EVERYONE,
    )


class ERC20SlotBuyingUseCase:
    def __init__(
            self,
            web3_adapter: IAppWeb3Provider,
            repository_factory: IRepositoryFactory,
            contract_manager: IContractManager,
            network: str,
            token: TokenDTO,
            ) -> None:
        self.__web3_adapter = web3_adapter
        self.__repository_factory = repository_factory
        self.__contract_manager = contract_manager
        self.__network_symbol = network
        self.__token = token
    

    async def pay_for_ERC20_slot_for_tg_user(
            self,
            telegram_id: int,
            password: str,
            pay_token_symbol: str,
            price: int,
            ):
        await self.__validate_input(telegram_id=telegram_id, password=password, price=price)
        token_repository = self.__repository_factory.token_repository
        pay_token = await token_repository.get_token_by_network_name_and_symbol(self.__network_symbol, pay_token_symbol)
        account_data = AppAccount(self.__web3_adapter, password, telegram_id, SEED_PHRASE).get_account_dto()
        token_service = Token(self.__web3_adapter, self.__contract_manager)
        service_factory = AccountServiceFactory(token=token_service)
        account = Account(account_data, service_factory)
        user_repository = self.__repository_factory.user_repository

        user = await user_repository.get_user_by_telegram_id(telegram_id)
        token_to_add: TokenDTO = await token_repository.get_token_by_network_name_and_symbol(self.__network_symbol, self.__token.symbol)
        if token_to_add:

            is_token_already_added = await user_repository.user_has_token(user.id, token_to_add.id)
            if is_token_already_added:
                raise TokenAlreadyBeenAddedError("This token has already been added.")
            
            if token_to_add.is_base:
                raise TokenAlreadyBeenAddedError("This token has already been added.")

        recipient_amount = price
        if user.referrer_id:
            referrer = await user_repository.get_user_by_id(user.referrer_id)
            referrer_address = await user_repository.get_active_address_by_telegram_id(referrer.tg_id)
            if referrer_address:
                referrer_amount = int(float(price) * REFERRER_PART_TO_ADD_ERC20)
                recipient_amount -= referrer_amount
                referrer.ref_income += referrer_amount
                await user_repository.update_user(referrer.id, referrer)
                await account.send_tokens(referrer_amount, referrer_address.address, pay_token)

        tx_hash = await account.send_tokens(int(recipient_amount), RECIPIENT, pay_token)

        user.tokens_limit += 1
        await user_repository.update_user(user.id, user)
        
        return tx_hash


    async def pay_for_ERC20_slot_for_everyone(
            self,
            telegram_id: int,
            password: str,
            pay_token_symbol: str,
            price: int,
            ):
        await self.__validate_input(telegram_id=telegram_id, password=password, price=price)
        token_repository = self.__repository_factory.token_repository
        pay_token = await token_repository.get_token_by_network_name_and_symbol(self.__network_symbol, pay_token_symbol)
        account_data = AppAccount(self.__web3_adapter, password, telegram_id, SEED_PHRASE).get_account_dto()
        token_service = Token(self.__web3_adapter, self.__contract_manager)
        service_factory = AccountServiceFactory(token=token_service)
        account = Account(account_data, service_factory)
        user_repository = self.__repository_factory.user_repository

        user = await user_repository.get_user_by_telegram_id(telegram_id)
        existing_token = await token_repository.get_token_by_network_name_and_symbol(self.__network_symbol, self.__token.symbol)
        
        if existing_token:
            if existing_token.is_base:
                raise TokenAlreadyBeenAddedError("The token has already been added")
            

        recipient_amount = price
        if user.referrer_id:
            referrer = await user_repository.get_user_by_id(user.referrer_id)
            referrer_address = await user_repository.get_active_address_by_telegram_id(referrer.tg_id)
            if referrer_address:
                referrer_amount = int(float(price) * REFERRER_PART_TO_ADD_ERC20_TO_EVERYONE)
                recipient_amount -= referrer_amount
                referrer.ref_income += referrer_amount
                await user_repository.update_user(referrer.id, referrer)
                await account.send_tokens(referrer_amount, referrer_address.address, pay_token)
        tx_hash = await account.send_tokens(int(recipient_amount), RECIPIENT, pay_token)

        return tx_hash


    async def __validate_input(self, telegram_id: int, password: str, price: int):
        telegram_id_field_name = "telegram_id"
        Validator.validate_number(telegram_id, telegram_id_field_name)
        Validator.is_more_than(telegram_id, 0, telegram_id_field_name)
        price_field_name = "price"
        Validator.validate_number(price, price_field_name)
        Validator.is_more_than(price, 0, price_field_name)
        price = float(price)
        Validator.validate_password(password)
        user_repository = self.__repository_factory.user_repository

        user = await user_repository.get_user_by_telegram_id(telegram_id)
        active_address, user_addresses = await asyncio.gather(
        user_repository.get_active_address_by_telegram_id(telegram_id),
        user_repository.get_addresses_by_user(user.id)
        )

        account_data = AppAccount(
            self.__web3_adapter, password, telegram_id, SEED_PHRASE
        ).get_account_dto()
        
        if not Validator.is_address_exist(account_data.address, user_addresses):
            raise AddressAlreadyExists("The address you are trying to create already exists.")

        if account_data.address != active_address.address:
            raise NotActiveAddressError("You are using an address from another wallet")