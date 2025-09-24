from domain.account.model import Account, AccountServiceFactory
from app.application.dto import TradeDTO
from app.application.service.common.port import IAppWeb3Provider, IAppTradeProvider, IContractManager
from app.application.service.model import Token, AppTrade, Validator


class GetTradeParametersUseCase:
    def __init__(
            self,
            web3_adapter: IAppWeb3Provider,
            trade_service: IAppTradeProvider,
            contract_manager: IContractManager
        ) -> None:
        self.__web3_adapter = web3_adapter
        self.__trade_service = trade_service
        self.__contract_manager = contract_manager


    async def get_trade_parameters(
            self,
            trade_parameters_data: TradeDTO
        ) -> TradeDTO:
        self.__validate_input(trade_parameters_data.amount_to_sell)
        trade_parameters_data.amount_to_sell = int(float(trade_parameters_data.amount_to_sell) * 10**trade_parameters_data.sell_token.decimal)
        token_service = Token(self.__web3_adapter, self.__contract_manager)
        trade_service = AppTrade(self.__trade_service)
        service_factory = AccountServiceFactory(token=token_service, trade_provider=trade_service)
        account = Account(service_factory=service_factory)

        trade_parameters = await account.get_trade_parameters(trade_parameters_data)

        return trade_parameters
    

    def __validate_input(self, amount_to_sell: int):
        amount_to_sell_field_name = "amount to sell"
        Validator.validate_number(amount_to_sell, amount_to_sell_field_name)
        Validator.is_more_than(amount_to_sell, 0, amount_to_sell_field_name)