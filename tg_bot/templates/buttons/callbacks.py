from aiogram.filters.callback_data import CallbackData


class DepositCallbackData(CallbackData, prefix="deposit"):
    action: str


class SendCallbackData(CallbackData, prefix="send"):
    action: str
    token: str


class ConfirmCallbackData(CallbackData, prefix="confirm"):
    action: str


class BalanceCallbackData(CallbackData, prefix="balance"):
    action: str


class StakeCallbackData(CallbackData, prefix="stake"):
    action: str


class NewAddressCallbackData(CallbackData, prefix="new_address"):
    action: str


class PaymentForNewAddressCallbackData(CallbackData, prefix="paymentAddress"):
    action: str


class PaymentForERC20CallbackData(CallbackData, prefix="paymentERC20"):
    action: str


class AddERC20(CallbackData, prefix="only"):
    action: str


class SwapCallbackData(CallbackData, prefix="swap"):
    action: str


class LanguageCallbackData(CallbackData, prefix="lang"):
    language: str


class BrubCallbackData(CallbackData, prefix="brub"):
    action: str


class BroadcastingCallbackData(CallbackData, prefix="broadcasting"):
    option: str


class AddButtonCallbackData(CallbackData, prefix="add_button"):
    action: str


class SendAdminMessageCallbackData(CallbackData, prefix="send_message"):
    action: str