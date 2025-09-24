import time
import asyncio
from web3 import AsyncWeb3, Web3
from web3.exceptions import BlockNotFound, BadFunctionCallOutput, ContractLogicError
from web3.contract import AsyncContract
from web3.types import ChecksumAddress
from eth_account.signers.local import LocalAccount
from eth_account.datastructures import SignedTransaction
from hexbytes import HexBytes
from domain.account.port import IWeb3Provider
from app.application.dto import AccountDTO, TokenDTO
from app.application.service.common import ContractsDTO
from infrastructure.operating_system import ContractManager
from domain.common.errors import InsufficientFundsError
from .errors import (
    FailedToConnectToNodeError,
    GasExceedsAllowanceError,
    BlockNotFoundError,
    TransferAmountExceedsBalanceError,
    InvalidTransactionFieldsError,
    TransactionPendingError,
    TransactionFailedError,
    InsufficientLiquidityError,
    NotERC20Token
    )


DEFAULT_TIMEOUT = 1200
GAS_MULTIPLIER = 5
GAS_PRICE_MULTIPLIER = 2

class Web3Adapter(IWeb3Provider):
    def __init__(self, provider_url: str) -> None:
        self.__web3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(provider_url))

    async def check_connection(self) -> bool:
        if not await self.__web3.is_connected():
            raise FailedToConnectToNodeError("Failed to connect to the blockchain node")
        
        return True
    

    async def get_ERC20_token(self, contract_address: str) -> TokenDTO:
        """Checks if a contract is an ERC20 token and returns its TokenDTO representation."""
        erc20_methods = ["name", "symbol", "decimals", "totalSupply"]
        try:
            erc20_abi = ContractManager.load_contract_abi_json(ContractsDTO.ERC20)
            contract = self.__web3.eth.contract(address=contract_address, abi=erc20_abi)
            for method in erc20_methods:
                if not hasattr(contract.functions, method):
                    return None
            
            name = await contract.functions.name().call()
            symbol = await contract.functions.symbol().call()
            decimals = await contract.functions.decimals().call()

            current_block = await self.__web3.eth.block_number

            return TokenDTO(
                id=0,
                name=name,
                symbol=symbol,
                address=contract_address,
                standard="erc20",
                decimal=decimals,
                network_id=1,
                is_base=False,
                last_checked_block=current_block,
            )

        except (BadFunctionCallOutput, ContractLogicError):
            raise NotERC20Token("The contract does not comply with the ERC20 standard")
        
        except Exception as e:
            raise ValueError(f"Error checking ERC20 compliance: {e}")


    def get_address(self, private_key: str) -> str:
        address = self.__web3.eth.account.from_key(private_key).address
        return address


    def get_contract(self, contract_address: str, contract_abi) -> AsyncContract:
        contract: AsyncContract = self.__web3.eth.contract(address=contract_address, abi=contract_abi)
        return contract
        

    def hash(self, text: str) -> bytes:
        """Compute the keccak-256 hash of the input data."""
        result = Web3.keccak(text=text)
        return result
    

    async def get_balance(self, address: str):
        balance_in_wei: int = await self.__web3.eth.get_balance(address)
        
        return balance_in_wei
    
    
    async def estimate_gas(self, transaction: dict, gas_multiplier: float = None) -> int:
        """Estimate gas for a transaction and add a buffer."""
        try:
            gas_multiplier = gas_multiplier if gas_multiplier else GAS_MULTIPLIER
            estimated_gas = await self.__web3.eth.estimate_gas(transaction)
            return estimated_gas * gas_multiplier
        
        except ValueError as e:
            if "gas required exceeds allowance" in str(e):
                raise GasExceedsAllowanceError("User transaction failed due to excessive gas requirements.")


    async def build_transaction(
        self,
        sender_address: str,
        to_address: str,
        value: int,
        data: bytes,
        nonce: int = None,
        gas_price=None
    ) -> dict:
        if not nonce:
            nonce = await self.__web3.eth.get_transaction_count(sender_address, "pending")

        if not gas_price:
            gas_price = await self.__web3.eth.gas_price * GAS_PRICE_MULTIPLIER

        tx_params = {
            "from": sender_address,
            "chainId": await self.__web3.eth.chain_id,
            "nonce": nonce,
            "to": to_address,
            "value": value,
            "data": data,
            "gasPrice": gas_price,
        }

        return tx_params


    def sign_transaction(self, account: AccountDTO, transaction: dict) -> HexBytes:
        """Sign the transaction with the provided account."""
        try:
            private_key = account.private_key
            account: LocalAccount = self.__web3.eth.account.from_key(private_key)
            signed_transaction: SignedTransaction = account.sign_transaction(transaction)
        except TypeError as e:
            if "Transaction had invalid fields: {'gas': None}" in str(e):
                raise GasExceedsAllowanceError("User transaction failed due to excessive gas requirements.")
        return signed_transaction.rawTransaction


    async def send_transaction(self, signed_transaction: HexBytes) -> HexBytes:
        """Send the signed transaction and handle any errors."""
        try:
            tx_hash = await self.__web3.eth.send_raw_transaction(signed_transaction)
            receipt = await self.__web3.eth.wait_for_transaction_receipt(tx_hash, timeout=DEFAULT_TIMEOUT)
            return receipt["transactionHash"].hex()

        except ValueError as e:
            if "insufficient funds" in str(e):
                raise InsufficientFundsError("User has insufficient funds for the transaction.")
            
            if "gas required exceeds allowance" in str(e):
                raise GasExceedsAllowanceError("User transaction failed due to excessive gas requirements.")

        except BlockNotFound:
            raise BlockNotFoundError("Block not found for the transaction.")


        except Exception as e:
            if "transfer amount exceeds balance" in str(e):
                raise TransferAmountExceedsBalanceError("User transaction failed as transfer amount exceeds balance.")
            
            if "Transaction had invalid fields" in str(e):
                raise InvalidTransactionFieldsError("User transaction failed due to invalid fields.")

            if "execution reverted: SPL" in str(e):
                raise InsufficientLiquidityError("There is not enough liquidity in the pool")

    
    async def check_transaction_status(self, tx_hash: str) -> bool:
        retries = 5
        delay = 10
        start_time = time.time()
        for attempt in range(retries):

            print(f"attempt number: {attempt + 1}")
            try:
                tx_receipt = await self.__web3.eth.get_transaction_receipt(tx_hash)
                
                if tx_receipt is None:
                    raise TransactionPendingError(f"Transaction {tx_hash} is still pending.")
                
                if tx_receipt['status'] != 1:
                    tx_hash_url = f"https://polygonscan.com/tx/{tx_hash}"
                    raise TransactionFailedError(f"Transaction failed. See details: {tx_hash_url}")

                return True
            
            except TransactionPendingError:
                if attempt < retries - 1:
                    print(f"Transaction {tx_hash} pending, retrying in {delay}s... (attempt {attempt + 1})")

            except Exception as error:
                if attempt + 1 >= retries:
                    raise error
            
            finally:
                print("---------------------------------")
                print(f"Time from first request: {time.time() - start_time}")
                start_sleep = time.time()
                await asyncio.sleep(delay)
                sleep_time = time.time() - start_sleep
                print(f"Sleep time: {sleep_time}")
                print("---------------------------------")


    def is_checksum_valid(self, address: str) -> bool:
        return Web3.is_checksum_address(address)
    
    
    def to_checksum_address(self, address: str) -> ChecksumAddress:
        return Web3.to_checksum_address(address)