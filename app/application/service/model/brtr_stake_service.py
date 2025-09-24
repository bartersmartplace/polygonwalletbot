from app.application.service.common.port import IAppWeb3Provider, IContractManager
from app.application.service.common import ContractsDTO
from app.application.service.common.error import NotEnoughMoneyForStakingError
from app.application.dto import TokenDTO, AccountDTO
from .transaction_service import Transaction


class BrtrStake:
    def __init__(
            self,
            web_adapter: IAppWeb3Provider,
            contract_manager: IContractManager,
            BRTR: TokenDTO,
            stBRTR: TokenDTO,
            ) -> None:
        self.__web3_adapter = web_adapter
        self.__erc20_contract_abi = contract_manager.load_contract_abi_json(ContractsDTO.ERC20)
        self.__stake_brtr_cantract_abi = contract_manager.load_contract_abi_json(ContractsDTO.STAKED_BRTR)
        self.__BRTR = BRTR
        self.__stBRTR =  stBRTR
        # minimal value to start staking is 100 brtr
        self.__MIN_STAKING_VALUE = 100 * 10**BRTR.decimal



    async def stake(self, account: AccountDTO, amount: float):
        BRTR_contract = self.__web3_adapter.get_contract(self.__BRTR.address, self.__erc20_contract_abi)
        stBRTR_contract = self.__web3_adapter.get_contract(self.__stBRTR.address, self.__stake_brtr_cantract_abi)
        amount = int(amount * 10**self.__BRTR.decimal)
        if amount < self.__MIN_STAKING_VALUE:
            raise NotEnoughMoneyForStakingError(f"Stacking can be started from {self.__MIN_STAKING_VALUE / 10**self.__BRTR.decimal} {self.__BRTR.symbol}")
        
        data_to_approve = BRTR_contract.functions.approve(self.__stBRTR.address, amount)._encode_transaction_data()
        approve_tx_params = await self.__web3_adapter.build_transaction(
            account.address,
            self.__BRTR.address,
            0,
            data_to_approve
            )
        
        approve_tx_hash = await Transaction.send_tx(
            self.__web3_adapter,
            approve_tx_params,
            account
        )
        print(f"Approve tx hash: {approve_tx_hash}")

        data_to_mint = stBRTR_contract.functions.mint(amount)._encode_transaction_data()
        mint_tx_params = await self.__web3_adapter.build_transaction(
            account.address,
            self.__stBRTR.address,
            0,
            data_to_mint,
            nonce=approve_tx_params['nonce']+ 1
            )
        
        mint_tx_hash = await Transaction.send_tx(
            self.__web3_adapter,
            mint_tx_params,
            account
        )
        print(f"Mint tx hash: {approve_tx_hash}")
        return mint_tx_hash


    async def get_from_stake(self, account: AccountDTO, amount: int):
        amount = int(amount * 10**self.__BRTR.decimal)
        stBRTR_contract = self.__web3_adapter.get_contract(self.__stBRTR.address, self.__stake_brtr_cantract_abi)
        data_to_burn_stBRTR = stBRTR_contract.functions.burn(amount)._encode_transaction_data()
        tx_param = await self.__web3_adapter.build_transaction(
            account.address,
            self.__stBRTR.address,
            0,
            data_to_burn_stBRTR
            )
        
        tx_hash = await Transaction.send_tx(
            self.__web3_adapter,
            tx_param,
            account
        )
        
        return tx_hash