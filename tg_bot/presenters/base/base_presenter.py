from domain.common.errors import AppError
from tg_bot.localization import _
from domain.common.errors import InsufficientFundsError
from app.application.service.common.error import (
    PasswordValidationError,
    AddressAlreadyExists,
    AddressNotFoundError,
    NotActiveAddressError,
    NotEnoughMoneyForStakingError,
    ValueIsNotNumberError,
    SmallValueError,
    TokenNotSupportedError,
    TokenNotFoundError,
    InvalidCharacterError,
    InvalidLengthError,
    MissingPrefixError,
    AddressDoesNotExistError,
    TokenAlreadyBeenAddedError,
)

from infrastructure.network.errors import (
    FailedToConnectToNodeError,
    GasExceedsAllowanceError,
    BlockNotFoundError,
    TransferAmountExceedsBalanceError,
    InvalidTransactionFieldsError,
    TransactionFailedError,
    TransactionPendingError,
    FeeNotSetError,
    NotSupportedExchangeError,
    InsufficientLiquidityError,
    NotERC20Token,
)


class BasePresenter:
    def __init__(self, language: str = "en"):
        self._ = lambda text: _(text, locale=language)
        self.ERRORS = {
            InsufficientFundsError: self._("There are not enough funds to complete this transaction."),
            PasswordValidationError: self._("The password you provided is invalid. Please check the format and try again."),
            AddressAlreadyExists: self._("The address you are trying to create already exists."),
            AddressDoesNotExistError: self._("The address you are trying to use does not exist."),
            NotEnoughMoneyForStakingError: self._("You do not have enough funds for staking. Please ensure your balance meets the minimum requirement."),
            AddressNotFoundError: self._("The requested address could not be found."),
            ValueIsNotNumberError: self._("The value entered is not a valid number. Please provide a numeric value."),
            SmallValueError: self._("The value you entered is too small. Please provide a larger value."),
            TokenNotSupportedError: self._("This token is not supported. Please check the token and try again."),
            TokenNotFoundError: self._("The specified token could not be found. Please verify the token symbol and try again."),
            InvalidLengthError: self._("The input length is invalid. Please check the input and try again."),
            MissingPrefixError: self._("The address is missing a required prefix. Please check the address and try again."),
            InvalidCharacterError: self._("The address contains invalid characters. Please check and correct the address format."),
            NotActiveAddressError: self._("The address you are trying to use is not active. Please check and try again."),
            FailedToConnectToNodeError: self._("Unable to connect to the blockchain node. Please try again later."),
            GasExceedsAllowanceError: self._("You don't have enough gas for this operation."),
            BlockNotFoundError: self._("The requested block could not be found"),
            TransferAmountExceedsBalanceError: self._("The transfer amount exceeds your available balance. Please check your balance and try again."),
            InvalidTransactionFieldsError: self._("The transaction contains invalid fields. Please check the transaction details and try again."),
            TransactionPendingError: self._("The transaction is still pending. Please wait for confirmation before proceeding."),
            TransactionFailedError: self._("The transaction failed due to an internal error. Please try again later."),
            FeeNotSetError: self._("A required fee has not been set for the transaction. Please provide the necessary fee and try again."),
            NotSupportedExchangeError: self._("The exchange pair you selected is not supported. Please choose a different exchange."),
            InsufficientLiquidityError: self._("There is not enough liquidity in the pool"),
            NotERC20Token: self._("The contract does not comply with the ERC20 standard"),
            TokenAlreadyBeenAddedError: self._("The token has already been added")
        }


    def get_start_message(self) -> str:
        return self._(
            "<b>Bot commands:</b>\n"
            "/assets - cryptocurrencies in wallet\n"
            "/stake - earn BRTR from staking\n"
            "/addresses - switch wallet\n"
            "/swap - token Exchange using Uniswap\n"
            "/settings - bot settings\n"
            "/referral - get your referral link\n\n"
            "<b>You can also use text commands:</b>\n\n"
            "💸 <b>Transfer tokens:</b>\n"
            "send [value] [token symbol] [User name or wallet address] [wallet password]\n\n"
            "Example 1:\n"
            "send 10 BRTR @polygonwalletbot Password\n"
            "Example 2:\n"
            "send 10 BRTR 0x17d3d1DA06688bC61592913921414bff09Bc570c Password\n\n"
            "💰 <b>Add BRTR to staking:</b>\n"
            "stake 100 Password\n\n"
            "🤑 Remove BRTR from staking:\n"
            "burn 100 Password"
        )


    def get_wait_message(self) -> str:
        return self._("⏳ Wait please...")
    

    def get_error_message(self, error: AppError) -> str:
        localized_message = self.ERRORS.get(type(error))

        if localized_message is None:
            return str(error)

        return str(localized_message)