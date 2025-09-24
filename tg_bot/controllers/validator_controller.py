from infrastructure.network.web3_adapter import Web3Adapter
from infrastructure.database import DAOFactory, RepositoryFactory
from app.application.use_case import (
    ValidatePasswordUseCase,
    GetUserUseCase,
    ValidateAddressUseCase,
    ValidateAmountToSendUseCase,
)
from tg_bot.constants import NETWORK_RPC_URL


class ValidatorController:
    def __init__(self, session, network_name: str = "Polygon"):
        self.__network_name = network_name
        self.__session = session
    
    async def validate_password(self, telegram_id, password: str) -> bool:
            repository_factory = RepositoryFactory(DAOFactory(self.__session))
            web3_adapter = Web3Adapter(NETWORK_RPC_URL)
            validator = ValidatePasswordUseCase(web3_adapter, repository_factory)
            check_result = await validator.validate_password(telegram_id=telegram_id,password=password)

            return check_result
    

    async def validate_recipient(
            self,
            tg_recipient: str = None,
            external_recipient: str = None
            ) -> str:
        address = None

        repository_factory = RepositoryFactory(DAOFactory(self.__session))
        if tg_recipient:
            get_active_address_use_case = GetUserUseCase(repository_factory)
            address = await get_active_address_use_case.get_active_address_for_tg_user(tg_username=tg_recipient)
            return address.address

        elif external_recipient:
            web3_adapter = Web3Adapter(NETWORK_RPC_URL)
            validate_address_use_case = ValidateAddressUseCase(web3_adapter)
            validate_address_use_case.validate_address(external_recipient)

            return external_recipient
    

    def validate_amount(self, amount: float) -> bool:
        validate_amount_use_case = ValidateAmountToSendUseCase()
        validate_amount_use_case.validate_amount_to_send(amount)

        return True