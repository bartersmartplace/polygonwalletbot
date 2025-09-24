from abc import ABC, abstractmethod

class ITradeProvider(ABC):
    @abstractmethod
    async def get_trade_parameters(self, trade_parameters):
        pass


    @abstractmethod
    async def make_trade(self, account, trade_parameters, slippage: float = None) -> str:
        pass