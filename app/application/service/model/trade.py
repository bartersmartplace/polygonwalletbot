from domain.account.port import ITradeProvider
from app.application.dto import TradeDTO, AccountDTO
from app.application.service.common.port import IAppTradeProvider


class AppTrade(ITradeProvider):
    def __init__(
            self,
            trade_service: IAppTradeProvider,
            ) -> None:
        self.__trade_provider = trade_service


    async def get_trade_parameters(
            self,
            trade_parameters: TradeDTO
            ) -> TradeDTO:
        amount_to_buy = await self.__trade_provider.get_sold_tokens_price(trade_parameters)
        trade_parameters.amount_to_buy = amount_to_buy

        return trade_parameters


    async def make_trade(
            self,
            account: AccountDTO,
            trade_parameters: TradeDTO,
            slippage: float = None
            ) -> str:
        tx_hash = await self.__trade_provider.make_trade(account, trade_parameters, slippage)
        
        return tx_hash