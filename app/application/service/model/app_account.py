from app.application.service.common.port import IAppWeb3Provider
from app.application.dto import AccountDTO


class AppAccount:
    def __init__(
            self,
            web3: IAppWeb3Provider,
            password: str,
            telegram_id: int,
            seed_phrase: str
            ):
        self.__private_key = self.__set_private_key(password, telegram_id, web3, seed_phrase)
        self.__address = web3.get_address(self.__private_key)


    def get_account_dto(self) -> AccountDTO:
        return AccountDTO(private_key=self.__private_key, address=self.__address)
    

    def __set_private_key(
            self,
            password: str,
            telegram_id: int,
            web3: IAppWeb3Provider,
            seed_phrase: str
            ) -> str:
        hashed_password = web3.hash(text=f"{password}").hex()
        combined_input_new = f"{telegram_id}{hashed_password}{seed_phrase}"
        private_key = web3.hash(text=combined_input_new).hex()
        return private_key