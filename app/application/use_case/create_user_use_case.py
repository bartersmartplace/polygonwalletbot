from app.application.service.common.port import IRepositoryFactory
from app.application.dto import UserDTO


class CreateUserUseCase:
    def __init__(
            self,
            repository_factory: IRepositoryFactory,
            ) -> None:
        self.__repository_factory = repository_factory

    
    async def create_user(
            self,
            telegram_id: int = None,
            tg_name: str = None,
            tg_username: str = None,
            referrer_id: int = None,
            ):
        user_repository = self.__repository_factory.user_repository

        if referrer_id and referrer_id != telegram_id:
            referrer: UserDTO = await user_repository.get_user_by_telegram_id(referrer_id)
            referrer_id = referrer.id

        user: UserDTO = await user_repository.get_user_by_telegram_id(telegram_id)
        if not user:
            user = UserDTO(
                id=0,
                tg_id=telegram_id,
                tg_name=tg_name,
                tg_username=tg_username,
                active_address_id=None,
                address_limit=1,
                language="en",
                is_admin=False,
                is_banned=False,
                referrer_id=referrer_id,
                ref_income=0,
                tokens_limit=1,
                )
            user = await user_repository.create_user(user)