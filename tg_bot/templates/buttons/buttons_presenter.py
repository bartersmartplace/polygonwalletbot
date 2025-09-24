from tg_bot.localization import _
from .text import (
DEPOSIT_TEXT,
SEND_TEXT,
CONFIRM_TEXT,
CANCEL_TEXT,
BACK_SYMBOL,
BACK_TEXT,
ADD_TEXT,
REMOVE_TEXT,
ADD_NEW_ADDRESS_TEXT,
PAY_TEXT,
ENG_TEXT,
RUS_TEXT,
GET_BRUB_TEXT,
RETURN_BRUB_TEXT,
USER_COUNT_TEXT,
MESSAGE_BROADCASTING_TEXT,
ADD_BUTTON_TEXT,
SEND_ADMIN_MESSAGE_TEXT,
ADD_TOKEN,
ONLY_FOR_ME,
PAY_FOR_LISTING
)


class ButtonPresenter:
    def __init__(self, language: str = "en"):
        self._ = lambda text: _(text, locale=language)

        self._buttons = {
            DEPOSIT_TEXT: self._("Deposit"),
            SEND_TEXT: self._("Send"),
            CONFIRM_TEXT: self._("Confirm"),
            CANCEL_TEXT: self._("Cancel"),
            BACK_SYMBOL: "<",
            BACK_TEXT: self._("Back"),
            ADD_TEXT: self._("Add"),
            REMOVE_TEXT: self._("Remove"),
            PAY_TEXT: self._("Pay"),
            ENG_TEXT: self._("ENGLISH"),
            RUS_TEXT: self._("RUSSIAN"),
            GET_BRUB_TEXT: self._("Get a BRUB"),
            RETURN_BRUB_TEXT: self._("Return BRUB"),
            ADD_NEW_ADDRESS_TEXT: self._("Generate New Address"),
            USER_COUNT_TEXT: self._("Number of users"),
            MESSAGE_BROADCASTING_TEXT: self._("Message broadcasting"),
            ADD_BUTTON_TEXT: self._("Add button"),
            SEND_ADMIN_MESSAGE_TEXT: self._("Send message"),
            ADD_TOKEN: self._("Add token"),
            ONLY_FOR_ME: self._("Only for me"),
            PAY_FOR_LISTING: self._("Pay for listing")
        }


    def get_button_text(self, button_key: str) -> str:
        """Fetches a localized button text."""
        return self._buttons.get(button_key, self._("Unknown button"))