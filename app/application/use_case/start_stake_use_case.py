import asyncio
from domain.account.model import Account, AccountServiceFactory
from domain.stake.model import Stake, StakeServiceFactory
from app.application.service.common.error import AddressDoesNotExistError, NotActiveAddressError
from app.application.service.common.port import IAppWeb3Provider, IRepositoryFactory, IContractManager
from app.application.service.model import Token, AppAccount, BrtrStake, Validator
from app.config import SEED_PHRASE


class StartStakingUseCase:
    def __init__(
            self,
            web3_adapter: IAppWeb3Provider,
            repository_factory: IRepositoryFactory,
            contract_manager: IContractManager
        ) -> None:
        self.__web3_adapter = web3_adapter
        self.__repository_factory = repository_factory
        self.__contract_manager = contract_manager


    async def start_staking_BRTR(
            self,
            telegram_id: int,
            password: str,
            network: str,
            amount: float
        ) -> str:
        await self.__validate_input(telegram_id=telegram_id, password=password, amount=amount)
        amount = float(amount)
        token_repository = self.__repository_factory.token_repository
        BRTR = await token_repository.get_token_by_network_name_and_symbol(network, "BRTR")
        stBRTR = await token_repository.get_token_by_network_name_and_symbol(network, "stBRTR")
        stake_service = BrtrStake(self.__web3_adapter, self.__contract_manager, BRTR, stBRTR)
        stake_service_factory = StakeServiceFactory(stake_service)
        account_data = AppAccount(self.__web3_adapter, password, telegram_id, SEED_PHRASE).get_account_dto()
        token_service = Token(self.__web3_adapter, self.__contract_manager)
        account_service_factory = AccountServiceFactory(token=token_service)
        account = Account(account_data, service_factory=account_service_factory)
        stake = Stake(account=account, service_factory=stake_service_factory)

        tx_hash = await stake.stake(BRTR, amount)
        
        return tx_hash
    

    async def __validate_input(self, telegram_id: int, password: str, amount: int):
        amount_field_name =  "stake amount"
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