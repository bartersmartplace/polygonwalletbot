from domain.stake.port import IStake
from domain.common.service import DomainServiceFactory

class StakeServiceFactory(DomainServiceFactory):
    def __init__(
            self,
            stake_service: IStake,
            ):
        self.__stake_service = stake_service


    @property
    def stake(self) -> IStake:
        """Returns an Trade service."""
        return self.__stake_service