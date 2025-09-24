from infrastructure.network.web3_adapter import Web3Adapter
from infrastructure.operating_system.contract_manager import ContractManager
from infrastructure.database import DAOFactory, RepositoryFactory
from app.application.use_case import (
    CreateAccountUseCase,
    GetBalanceUseCase,
    NewAddressBuyingUseCase,
    SendTokenUseCase
)
from tg_bot.constants import NETWORK_RPC_URL

class AddressController:
    def __init__(self, session, network_name: str = "Polygon"):
        self.__session = session
        self.__network_name = network_name

        
    async def create_account(self, telegram_id: int, password: str, tg_name: str = None, tg_username: str = None) -> str:
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        create_account_use_case = CreateAccountUseCase(
            web3_adapter=web3_adapter,
            repository_factory=repository_factory,
        )
        return await create_account_use_case.generate_evm_address_for_tg_user(
            telegram_id=telegram_id, password=password, tg_name=tg_name, tg_username=tg_username
        )


    async def buy_new_address(self, telegram_id: int, password: str) -> str:
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        new_address_buying_use_case = NewAddressBuyingUseCase(
            web3_adapter=web3_adapter,
            repository_factory=repository_factory,
            contract_manager=ContractManager,
            network=self.__network_name
        )
        return await new_address_buying_use_case.pay_for_new_address_for_tg_users(
            telegram_id=telegram_id, password=password
        )
    

    async def send_tokens(
              self,
              telegram_id: int,
              password: str,
              token_symbol: str,
              amount: float,
              tg_recipient: str = None,
              external_recipient: str = None
              ):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        send_tokens_use_case = SendTokenUseCase(
                web3_adapter=web3_adapter,
                repository_factory=repository_factory,
                contract_manager=ContractManager,
                )
        
        if tg_recipient:
            tx_hash = await send_tokens_use_case.send_tokens_to_username(
                    telegram_id,
                    password,
                    self.__network_name,
                    token_symbol,
                    amount,
                    tg_recipient
            )

            return tx_hash
        
        if external_recipient:
            tx_hash = await send_tokens_use_case.send_tokens_to_external_address(
                    telegram_id,
                    password,
                    self.__network_name,
                    token_symbol,
                    amount,
                    external_recipient
            )

            return tx_hash


    async def get_account_balance(self, telegram_id: int):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        get_balance_use_case = GetBalanceUseCase(
            web3_adapter=web3_adapter,
            repository_factory=repository_factory,
                contract_manager=ContractManager,
        )

        return await get_balance_use_case.get_account_balance_for_tg_user(telegram_id=telegram_id) 


    async def get_token_balance_for_tg_user(self, telegram_id: int, token_symbol: str):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        get_balance_use_case = GetBalanceUseCase(
            web3_adapter=web3_adapter,
            repository_factory=repository_factory,
                contract_manager=ContractManager,
        )

        return await get_balance_use_case.get_token_balance_for_tg_user(telegram_id, self.__network_name, token_symbol)