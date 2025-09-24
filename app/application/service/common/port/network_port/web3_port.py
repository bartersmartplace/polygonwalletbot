from typing import Protocol
from app.application.dto import AccountDTO, TokenDTO


class IAppWeb3Provider(Protocol):
    def get_address(self, private_key: str) -> str:
        """get addres in EVM network"""
        pass


    def hash(self, text: str) -> bytes:
        """Get hash"""
        pass
    

    async def get_ERC20_token(self, contract_address: str) -> TokenDTO:
        pass

    
    def get_contract(self, contract_address: str, contract_abi):
        """Get contract abi"""
        pass
    

    def is_checksum_valid(self, address: str) -> bool:
        """Checksum checking"""
        pass


    async def get_balance(self, address: str):
        pass
    
    
    async def build_transaction(
        self,
        sender_address: str,
        to_address: str,
        value: int,
        data: bytes,
        nonce: int = None,
        gas_price=None
    ) -> dict:
        """Build EVM transaction"""
        pass

    
    async def estimate_gas(self, transaction: dict, gas_multiplier: float = None) -> int:
        """Estimate gas for transaction"""
        pass

    
    def sign_transaction(self, account: AccountDTO, transaction: dict):
        """Connect transaction with private key"""
        pass

    
    async def send_transaction(self, signed_transaction):
        """Send transaction to web3"""
        pass

    
    async def check_transaction_status(self, tx_hash: str) -> bool:
        """Check transaction status"""
        pass


    def to_checksum_address(self, address: str) -> str:
        """Convert to checksum"""
        pass