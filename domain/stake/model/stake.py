from .stake_service_factory import StakeServiceFactory
from ...account import Account

class Stake:
    def __init__(self, account: Account, service_factory: StakeServiceFactory):
        self.__account = account
        self.__service_factory = service_factory


    async def stake(self, token, amount):
        await self.__account.validate_sufficient_balance(amount, token)
        account = self.__account.get_account_data()
        tx__hash = await self.__service_factory.stake.stake(account, amount)
        
        return tx__hash


    async def unstake(self, token, amount):
        await self.__account.validate_sufficient_balance(amount, token)
        account = self.__account.get_account_data()
        tx_hash = await self.__service_factory.stake.get_from_stake(account, amount)
        
        return tx_hash