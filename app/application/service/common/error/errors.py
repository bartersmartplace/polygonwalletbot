from domain.common.errors import AppError


class PasswordValidationError(AppError):
    pass


class AddressAlreadyExists(AppError):
    pass


class AddressDoesNotExistError(AppError):
    pass


class NotEnoughMoneyForStakingError(AppError):
    pass


class MaxAddressesExistError(AppError):
    pass


class AddressNotFoundError(AppError):
    pass


class ValueIsNotNumberError(AppError):
    pass


class SmallValueError(AppError):
    pass


class TokenNotSupportedError(AppError):
    pass


class TokenNotFoundError(AppError):
    pass


class InvalidLengthError(AppError):
    pass


class MissingPrefixError(AppError):
    pass


class InvalidCharacterError(AppError):
    pass


class NotActiveAddressError(AppError):
    pass


class TokenAlreadyBeenAddedError(AppError):
    pass