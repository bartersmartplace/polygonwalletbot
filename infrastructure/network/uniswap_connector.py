from typing import Union
from eth_typing.evm import Address, ChecksumAddress
import time
from app.application.dto import TokenDTO, AccountDTO, TradeDTO
from infrastructure.database import RepositoryFactory
from infrastructure.operating_system import ContractManager
from app.application.service.common import ContractsDTO
from app.application.service.model import Transaction
from .web3_adapter import Web3Adapter
from .errors import FeeNotSetError, NotSupportedExchangeError


# constants
AddressLike = Union[Address, ChecksumAddress]
QUOTER_CONTRACT_ADDRESS = "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"
QUOTER_CONTRACT_ABI = ContractManager.load_contract_abi_json(ContractsDTO.QUOTER)
ROUTER_CONTRACT_ADDRESS = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
ROUTER_CONTRACT_ABI = ContractManager.load_contract_abi_json(ContractsDTO.ROUTER)
UNISWAP_GAS_MARGIN = 1.2
SLIPPAGE_DEFAULT = 0.01


class UniswapConnector:
    def __init__(
            self,
            web3_adapter: Web3Adapter,
            repository_factory: RepositoryFactory
            ) -> None:
        self.__web3 = web3_adapter
        self.__pool_repository = repository_factory.pool_repository
        self.__quoter = web3_adapter.get_contract(QUOTER_CONTRACT_ADDRESS, QUOTER_CONTRACT_ABI)
        self.__router = web3_adapter.get_contract(ROUTER_CONTRACT_ADDRESS, ROUTER_CONTRACT_ABI)


    async def get_sold_tokens_price(
            self,
            trade_parameters: TradeDTO
            ) -> int:
        pool = await self.__pool_repository.find_pool_by_tokens(trade_parameters.sell_token, trade_parameters.buy_token)
        if not pool:
            raise NotSupportedExchangeError("The exchange is not supported for this pair")
        
        fee = pool.fee
        price = await self.__get_price_input(trade_parameters.sell_token,
                                             trade_parameters.buy_token,
                                             trade_parameters.amount_to_sell,
                                             fee
                                             )

        return price


    async def make_trade(
            self,
            account: AccountDTO,
            trade_parameters: TradeDTO,
            slippage: float = None
            ) -> str:

        slippage = slippage if slippage else SLIPPAGE_DEFAULT
        pool = await self.__pool_repository.find_pool_by_tokens(trade_parameters.sell_token, trade_parameters.buy_token)

        if not pool:
            raise NotSupportedExchangeError("The exchange is not supported for this pair")
        
        erc20_contract_abi = ContractManager.load_contract_abi_json(ContractsDTO.ERC20)
        token_contract = self.__web3.get_contract(trade_parameters.sell_token.address, erc20_contract_abi)
        data_to_approve = token_contract.functions.approve(ROUTER_CONTRACT_ADDRESS, trade_parameters.amount_to_sell)._encode_transaction_data()
        approve_tx_params = await self.__web3.build_transaction(
            account.address,
            trade_parameters.sell_token.address,
            0,
            data_to_approve
            )
        approve_tx_hash = await Transaction.send_tx(
            self.__web3,
            approve_tx_params,
            account
        )
        print(f"Approve tx hash: {approve_tx_hash}")

        fee = pool.fee
        sqrtPriceLimitX96 = 0
        price = await self.__get_price_input(
                    trade_parameters.sell_token, trade_parameters.buy_token, trade_parameters.amount_to_sell, fee=fee
        )
        min_tokens_bought = int((1 - slippage) * price)
        
        tx_data = self.__router.functions.exactInputSingle(
            (
                trade_parameters.sell_token.address, # tokenIn
                trade_parameters.buy_token.address,  # tokenOut
                fee,                                 # fee
                account.address,                     # recipient
                self.__deadline(),                   # deadline
                trade_parameters.amount_to_sell,     # amountIn
                min_tokens_bought,                   # amountOutMinimum
                sqrtPriceLimitX96                    # sqrtPriceLimitX96
            )
        )._encode_transaction_data()
        
        tx_params = await self.__web3.build_transaction(
            sender_address=account.address,
            to_address=ROUTER_CONTRACT_ADDRESS,
            value=0,
            data=tx_data,
            gas_price=None,
            nonce=approve_tx_params['nonce']+ 1
        )

        trade_tx_hash = await Transaction.send_tx(
            self.__web3,
            tx_params,
            account
        )
        print(f"Trade tx hash: {approve_tx_hash}")
        return trade_tx_hash
    

    async def __get_price_input(
            self,
            sell_token: TokenDTO,
            buy_token: TokenDTO,
            amount_to_sell_in_wei: int,
            fee: int
            ) -> int:
        if fee is None:
            raise FeeNotSetError("No fee set")
        
        sqrtPriceLimitX96 = 0
        price_in_wei = await self.__quoter.functions.quoteExactInputSingle(
                sell_token.address, buy_token.address, fee, amount_to_sell_in_wei, sqrtPriceLimitX96
            ).call()
        
        return price_in_wei
    

    def __deadline(self) -> int:
        """Get a predefined deadline. 10min by default (same as the Uniswap SDK)."""
        return int(time.time()) + 10 * 60