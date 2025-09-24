from app.application.service.common.port import IAppWeb3Provider, IContractManager
from app.application.dto import AccountDTO, TokenDTO
from .transaction_service import Transaction


class Token:
    def __init__(
            self,
            web3_adapter: IAppWeb3Provider,
            contract_manager: IContractManager
            ) -> None:
        self.__web3_adapter = web3_adapter
        self.__contract_manager = contract_manager


    async def get_token_balance(
            self,
            account: AccountDTO,
            token: TokenDTO
            ) -> int:
        contract_abi = self.__contract_manager.load_contract_abi_json(token.standard)
        contract = self.__web3_adapter.get_contract(token.address, contract_abi)
        balance_in_wei = await contract.functions.balanceOf(account.address).call()

        return balance_in_wei
    

    async def get_native_token_balance(self, account: AccountDTO):
        balance_in_wei = await self.__web3_adapter.get_balance(account.address)

        return balance_in_wei


    async def send_erc20_tokens(
        self,
        account: AccountDTO,
        recipient_address: str,
        token: TokenDTO,
        value_in_wei: int,
    ) -> str:
        contract_abi = self.__contract_manager.load_contract_abi_json(token.standard)
        contract = self.__web3_adapter.get_contract(token.address, contract_abi)
        tx_data = contract.functions.transfer(recipient_address, value_in_wei)._encode_transaction_data()

        tx_params = await self.__web3_adapter.build_transaction(
            sender_address=account.address,
            to_address=token.address,
            value=0,
            data=tx_data
        )
        tx_hash = await Transaction.send_tx(
            self.__web3_adapter,
            tx_params,
            account
        )

        return tx_hash
    

    async def send_native_token(
        self,
        account: AccountDTO,
        recipient_address: str,
        value_in_wei: int,
    ) -> str:
        tx_params = await self.__web3_adapter.build_transaction(
            sender_address=account.address,
            to_address=recipient_address,
            value=value_in_wei,
            data=b""
        )
        tx_hash = await Transaction.send_tx(
            self.__web3_adapter,
            tx_params,
            account
        )

        return tx_hash