from ...common.errors import InsufficientFundsError
from .account_service_factory import AccountServiceFactory
from ...common.port import TokenData


class Account:
    def __init__(self, account = None, service_factory: AccountServiceFactory = None):
        self.__account = account
        self.__service_factory = service_factory


    def get_account_data(self):
        return self.__account


    async def validate_sufficient_balance(self, amount: float, token) -> bool:
        """Check if the account has enough balance for the specified amount."""
        balance = await self.get_token_balance(token)
        if balance < amount:
            raise InsufficientFundsError("Insufficient balance to complete the transaction.")
        
        return True


    async def send_tokens(self, amount: float, to_address: str, token: TokenData) -> str:
        """Send tokens using the account and return the transaction hash, after validating balance."""
        await self.validate_sufficient_balance(amount, token)
        
        if token.address:
            tx_hash = await self.__service_factory.token.send_erc20_tokens(
                self.__account, to_address, token, amount
            )
        else:
            tx_hash = await self.__service_factory.token.send_native_token(
                self.__account, to_address, amount
            )

        return tx_hash


    async def get_token_balance(self, token: TokenData) -> int:
        """Get the token balance of the account."""
        if token.address:
            balance_in_wei = await self.__service_factory.token.get_token_balance(self.__account, token)
        else:
            balance_in_wei = await self.__service_factory.token.get_native_token_balance(self.__account)

        return balance_in_wei


    async def get_trade_parameters(self, trade_parameters):
        """"Get trade parameters"""
        amount_to_buy = await self.__service_factory.trade.get_trade_parameters(trade_parameters)

        return amount_to_buy


    async def trade(self, trade_parameters) -> str:
        """exchange tokens"""
        tx_hash = await self.__service_factory.trade.make_trade(self.__account, trade_parameters)
        
        return tx_hash