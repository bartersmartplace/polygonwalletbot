from app.application.service.common.port import IRepositoryFactory, IAppWeb3Provider
from app.application.service.common.error import MaxAddressesExistError, AddressAlreadyExists
from app.application.dto import UserDTO
from app.application.service.model import AppAccount, Validator
from app.config import SEED_PHRASE


class CreateAccountUseCase:
    def __init__(
            self,
            web3_adapter: IAppWeb3Provider,
            repository_factory: IRepositoryFactory,
            ) -> None:
        self.__web3_adapter = web3_adapter
        self.__repository_factory = repository_factory


    async def generate_evm_address_for_tg_user(
            self,
            telegram_id: int,
            password: str,
            tg_name: str = None,
            tg_username: str = None
            ) -> str:
        self.__validate_input(telegram_id=telegram_id, password=password)

        account = AppAccount(self.__web3_adapter, password, telegram_id, SEED_PHRASE).get_account_dto()
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
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
                referrer_id=None,
                ref_income=0,
                tokens_limit=1,
                )
            user = await user_repository.create_user(user)
        user_addresses = await user_repository.get_addresses_by_user(user.id)

        if user.address_limit <= len(user_addresses):
            raise MaxAddressesExistError("The maximum number of generated addresses has been reached")
        
        is_address_exist = Validator.is_address_exist(account.address, user_addresses)
        if is_address_exist:
            raise AddressAlreadyExists("You already have an address for such a password")
        
        await user_repository.add_user_address(user.id, account.address)

        return account.address
    

    def __validate_input(self, telegram_id: int, password: str):
        telegram_id_field_name = "telegram_id"
        Validator.validate_number(telegram_id, telegram_id_field_name)
        Validator.is_more_than(telegram_id, 0, telegram_id_field_name)
        Validator.validate_password(password)