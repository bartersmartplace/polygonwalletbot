from domain.common.errors import AppError


class FailedToConnectToNodeError(AppError):
    pass


class GasExceedsAllowanceError(AppError):
    pass


class BlockNotFoundError(AppError):
    pass


class TransferAmountExceedsBalanceError(AppError):
    pass


class InvalidTransactionFieldsError(AppError):
    pass


class TransactionPendingError(AppError):
    pass


class TransactionFailedError(AppError):
    pass


class FeeNotSetError(AppError):
    pass


class InsufficientLiquidityError(AppError):
    pass


class NotSupportedExchangeError(AppError):
    pass


class NotERC20Token(AppError):
    pass