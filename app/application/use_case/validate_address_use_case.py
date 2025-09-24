from typing import List
from app.application.dto import AddressDTO, TokenDTO
from app.application.service.common.error import AddressNotFoundError
from app.application.service.common.port import IAppWeb3Provider
from app.application.service.model import Validator


class ValidateAddressUseCase:
    def __init__(
            self,
            web3_adapter: IAppWeb3Provider,
        ) -> None:
        self.__web3_adapter = web3_adapter


    def validate_address(
           self,
           address: str
           ) -> bool:
        address = Validator.is_correct_address(self.__web3_adapter, address)

        return True


    def address_exist(
            self,
            address: str,
            addresses_list: List[AddressDTO]
            ) -> bool:
        if not Validator.is_address_exist(address, addresses_list):
            raise AddressNotFoundError("There is no such address.")
        
        return True


    def get_ERC20_token(
        self,
        address: str,
        ) -> TokenDTO:
        address = Validator.is_correct_address(self.__web3_adapter, address)
        erc_20 = self.__web3_adapter.get_ERC20_token(address)
        return erc_20