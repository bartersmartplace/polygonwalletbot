from domain.common.port.token_port import ITokenService
from domain.common.service import DomainServiceFactory
from domain.account.port import ITradeProvider


class AccountServiceFactory(DomainServiceFactory):
    def __init__(
            self,
            token: ITokenService = None,
            trade_provider: ITradeProvider = None
            ):
        super().__init__(token)
        self._trade_provider = trade_provider


    @property
    def trade(self) -> ITradeProvider:
        """Returns an Trade service."""
        return self._trade_provider