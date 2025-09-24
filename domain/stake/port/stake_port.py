from abc import ABC, abstractmethod


class IStake(ABC):
    @abstractmethod
    async def stake(self, account, amount: int) -> str:
        pass

    @abstractmethod
    async def get_from_stake(self, account, amount: int) -> str:
        pass