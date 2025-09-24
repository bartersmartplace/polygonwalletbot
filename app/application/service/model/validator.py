import re
from typing import List
from app.application.dto import AddressDTO
from app.application.service.common.port.network_port import IAppWeb3Provider
from app.application.service.common.error import (
    PasswordValidationError,
    ValueIsNotNumberError,
    SmallValueError, 
    InvalidLengthError,
    MissingPrefixError,
    InvalidCharacterError,
    )


class Validator:
    """Utility class for various input validations."""
    
    @staticmethod
    def validate_number(value, field_name: str = "Value") -> bool:
        if isinstance(value, (int, float)):
            return True
        
        if isinstance(value, str):
            try:
                float(value)
                return True
            except ValueError:
                pass
        
        raise ValueIsNotNumberError(f"{field_name} must be a number.")


    @staticmethod
    def is_more_than(value: int, min_value: float, field_name: str = "Value") -> bool:
        value = float(value)
        if value <= min_value:
            raise SmallValueError(f"{field_name} must be more than {min_value}.")
        
        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            raise PasswordValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', password):
            raise PasswordValidationError("Password must contain at least one digit.")
        if not re.search(r'[A-Z]', password):
            raise PasswordValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[\W_]', password):
            raise PasswordValidationError("Password must contain at least one special character.")
        
        return True


    @staticmethod
    def is_correct_address(web3_adapter: IAppWeb3Provider, address: str):
        if len(address) != 42:
            raise InvalidLengthError("Invalid address length.")
        
        if not address.startswith('0x'):
            raise MissingPrefixError("Address must start with '0x'.")
        
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            raise InvalidCharacterError("Address contains invalid characters.")

        if not web3_adapter.is_checksum_valid(address):
            return web3_adapter.to_checksum_address(address)
        
        return address


    @staticmethod
    def is_address_exist(new_address: str, address_list: List[AddressDTO]):
        for address in address_list:
            if new_address == address.address:
                return address
        
        return False