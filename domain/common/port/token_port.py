from abc import ABC, abstractmethod
from .web3_port import IWeb3Provider


class ITokenService(ABC):
    @abstractmethod
    async def get_token_balance(self, web3_adapter: IWeb3Provider, account, token):
        """Returns the token balance."""
        pass
    

    @abstractmethod
    async def get_native_token_balance(self, account):
        pass


    @abstractmethod
    async def send_erc20_tokens(
        self,
        account,
        recipient_address: str,
        ERC20DTO,
        value_in_wei: int,
    ) -> str:
        """Sends tokens and returns the transaction hash as a hex string."""
        pass


    @abstractmethod
    async def send_native_token(
        self,
        account,
        recipient_address: str,
        value_in_wei: int,
    ) -> str:
        """Sends tokens and returns the transaction hash as a hex string."""
        pass