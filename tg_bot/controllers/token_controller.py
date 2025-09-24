from infrastructure.network.web3_adapter import Web3Adapter
from infrastructure.network.uniswap_connector import UniswapConnector
from infrastructure.operating_system.contract_manager import ContractManager
from infrastructure.database import DAOFactory, RepositoryFactory
from app.application.service.common.error import TokenNotFoundError 
from app.application.dto import TradeDTO, TokenDTO
from app.application.use_case import (
    GetTokensUseCase,
    GetTradeParametersUseCase,
    MakeTradeUseCase,
    ValidateAddressUseCase,
    ERC20SlotBuyingUseCase,
    AddTokenUseCase,
)
from tg_bot.constants import NETWORK_RPC_URL

class TokenController:
    def __init__(self, session, network_name: str = "Polygon"):
        self.__network_name = network_name
        self.__session = session

    async def get_sendable_tokens(self, telegram_id: int):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        get_sendable_tokens_use_case = GetTokensUseCase(repository_factory)
        
        return await get_sendable_tokens_use_case.get_sendable_tokens(telegram_id)


    async def get_user_tokens(self, telegram_id):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        get_tokens_use_case = GetTokensUseCase(repository_factory)
        
        return await get_tokens_use_case.get_user_tokens(telegram_id)


    async def get_ERC20_token(self, address: str):
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        validate_address_use_case = ValidateAddressUseCase(web3_adapter)
        
        return await validate_address_use_case.get_ERC20_token(address)
    

    async def buy_slot_for_new_user_token(
            self,
            telegram_id: int,
            password: str,
            pay_token_symbol: str,
            price: int,
            token: TokenDTO,
            ):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        buy_slot_use_case = ERC20SlotBuyingUseCase(web3_adapter, repository_factory, ContractManager, self.__network_name, token)
        tx_hash = await buy_slot_use_case.pay_for_ERC20_slot_for_tg_user(telegram_id, password, pay_token_symbol, price)

        return tx_hash
    

    async def buy_slot_for_new_base_token(
            self,
            telegram_id: int,
            password: str,
            pay_token_symbol: str,
            price: int,
            token: TokenDTO,
            ):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        buy_slot_use_case = ERC20SlotBuyingUseCase(web3_adapter, repository_factory, ContractManager, self.__network_name, token)
        tx_hash = await buy_slot_use_case.pay_for_ERC20_slot_for_everyone(telegram_id, password, pay_token_symbol, price)

        return tx_hash
    

    async def add_user_token(self, telegram_id, token: TokenDTO):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        add_user_token_use_case = AddTokenUseCase(repository_factory)
        await add_user_token_use_case.add_user_token(telegram_id, token, self.__network_name)

        return True
    

    async def add_base_token(self, token: TokenDTO):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        add_user_token_use_case = AddTokenUseCase(repository_factory)
        await add_user_token_use_case.add_base_token(token, self.__network_name)

        return True


    async def get_trade_parameters(
            self,
            sell_token_symbol: str,
            buy_token_symbol: str,
            amount_to_sell: float,
            ) -> str:
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        network_repository = repository_factory.network_repository
        network = await network_repository.get_network_by_name(self.__network_name)
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        uniswap_connector = UniswapConnector(web3_adapter, repository_factory)
        trade_use_case = GetTradeParametersUseCase(web3_adapter, uniswap_connector, ContractManager)
        token_repository = repository_factory.token_repository

        sell_token = await token_repository.get_token_by_network_name_and_symbol(network.name, sell_token_symbol.upper())
        if not sell_token:
            raise TokenNotFoundError(
                ("Token not found for network: {network}, symbol: {symbol}").format(
                    network=network.name, symbol=sell_token_symbol
                )
            )

        buy_token = await token_repository.get_token_by_network_name_and_symbol(
            network.name, buy_token_symbol.upper()
        )
        if not buy_token:
            raise TokenNotFoundError(
                ("Token not found for network: {network}, symbol: {symbol}").format(
                    network=network.name, symbol=buy_token_symbol
                )
    )
        
        trade = TradeDTO(
            sell_token=sell_token,
            amount_to_sell=amount_to_sell,
            buy_token=buy_token,
            amount_to_buy=None)
        trade = await trade_use_case.get_trade_parameters(trade)

        return trade
    

    async def make_trade_parameters(
            self,
            telegram_id: int,
            password: str,
            trade: TradeDTO
            ) -> str:
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        uniswap_connector = UniswapConnector(web3_adapter, repository_factory)
        trade_use_case = MakeTradeUseCase(web3_adapter, repository_factory, uniswap_connector, ContractManager)
        
        tx_hash = await trade_use_case.make_trade(telegram_id, password, trade)

        return tx_hash