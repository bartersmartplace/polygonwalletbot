from typing import Protocol
from app.application.dto import TradeDTO, AccountDTO


class IAppTradeProvider(Protocol):
    async def get_sold_tokens_price(
                self,
                trade_parameters: TradeDTO
                ) -> int:
        pass


    async def make_trade(
            self,
            account: AccountDTO,
            trade_parameters: TradeDTO,
            slippage: float = None
            ) -> str:
        pass