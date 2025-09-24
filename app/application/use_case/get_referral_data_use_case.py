from app.application.dto import ReferralDTO
from app.application.service.common.port import IRepositoryFactory


class GetReferralDataUseCase:
    def __init__(
            self,
            repository_factory: IRepositoryFactory
            ) -> None:
        self.__repository_factory = repository_factory

    
    async def get_referral_data(self, telegram_id: int):
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
        referrals = await user_repository.get_referrals(user.id)
        ref_data = ReferralDTO(
            ref_counts=len(referrals) if referrals else 0,
            ref_income=user.ref_income
        )   

        return ref_data