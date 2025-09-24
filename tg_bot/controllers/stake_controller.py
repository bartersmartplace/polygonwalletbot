import asyncio
from typing import Tuple
from infrastructure.network.web3_adapter import Web3Adapter
from infrastructure.network.stakers_data import StakeDataProvider
from infrastructure.operating_system.contract_manager import ContractManager
from infrastructure.database import DAOFactory, RepositoryFactory
from app.application.dto import BalanceDTO
from app.application.use_case import (
    GetBalanceUseCase,
    StartStakingUseCase,
    StopStakingUseCase
)
from tg_bot.constants import NETWORK_RPC_URL


class StakeController:
    def __init__(self, session, network_name: str = "Polygon"):
        self.__network_name = network_name
        self.__session = session

    async def get_stake_base_info(self, telegram_id: int) -> Tuple[BalanceDTO, BalanceDTO, int, int]:
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        get_balance_use_case = GetBalanceUseCase(
            web3_adapter=web3_adapter,
            repository_factory=repository_factory,
            contract_manager=ContractManager,
        )

        stBRTR_task = get_balance_use_case.get_token_balance_for_tg_user(
            telegram_id=telegram_id,
            network_name=self.__network_name,
            symbol="stBRTR",
        )
        BRTR_task = get_balance_use_case.get_token_balance_for_tg_user(
            telegram_id=telegram_id,
            network_name=self.__network_name,
            symbol="BRTR",
        )
        stakers_count_task = StakeDataProvider.get_stakers_count()
        staked_data_task = StakeDataProvider.get_stake_data()

        stBRTR_balance, BRTR_balance, stakers_count, staked_data = await asyncio.gather(
            stBRTR_task, BRTR_task, stakers_count_task, staked_data_task
        )
        totalValueLocked = int(staked_data["totalValueLocked"])

        return stBRTR_balance, BRTR_balance, stakers_count, totalValueLocked
    

    async def start_stake_brtr_use_case(
            self,
            telegram_id: int,
            password: str,
            amount: float        
            ):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        start_staking_use_case = StartStakingUseCase(web3_adapter, repository_factory, ContractManager)
        tx_hash = await start_staking_use_case.start_staking_BRTR(telegram_id=telegram_id, password=password, network=self.__network_name, amount=amount)

        return tx_hash


    async def stop_stake_brtr_use_case(
            self,
            telegram_id: int,
            password: str,
            amount: float
            ):
        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        web3_adapter = Web3Adapter(NETWORK_RPC_URL)
        start_staking_use_case = StopStakingUseCase(web3_adapter, repository_factory, ContractManager)
        tx_hash = await start_staking_use_case.unstake_BRTR(telegram_id=telegram_id, password=password, network=self.__network_name, amount=amount)

        return tx_hash