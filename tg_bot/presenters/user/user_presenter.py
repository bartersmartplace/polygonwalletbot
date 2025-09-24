from typing import List
from app.application.dto import AddressDTO, ReferralDTO
from tg_bot.localization import _
from tg_bot.presenters.utils import format_number_value


class UserPresenter:
    def __init__(self, language: str = "en") -> None:
        self._ = lambda text: _(text, locale=language)


    def get_addresses_list_message(self, address_list: List[AddressDTO]) -> str:
        if address_list:
            message = self._("Copy and paste the address you want to select and use:\n")
            for i, address in enumerate(address_list, start=1):
                message += f"{i}) `{address.address}`\n"
        else:
            message = self._("You don't have any addresses.")

        return message


    def get_active_address_update_message(self) -> str:
        return self._("Wallet has been changed.")


    def get_active_address_message(self, active_address: AddressDTO) -> str:
        return self._(
            "To top up your balance, transfer money to this address:\n"
            "`{address}`"
        ).format(address=active_address.address)


    def get_referal_link_message(self, 
                                 bot_username: str, 
                                 user_id: int, 
                                 ref_data: ReferralDTO,
                                 token_decimal: int,
                                 token_symbol: str) -> str:
        referral_link = f"https://t.me/{bot_username}?start={user_id}"
        return self._(
            "Invited - {invited}\n"
            "Earned - {earned} {symbol}\n\n"
            "Referral link, copy and share:\n"
            "`{link}`"
        ).format(
            invited=ref_data.ref_counts,
            earned=format_number_value(ref_data.ref_income / 10 ** token_decimal),
            symbol=token_symbol,
            link=referral_link
    )


    def get_choose_language_message(self) -> str:
        return self._("Choose language.")


    def get_language_changed_message(self, language: str) -> str:
        return self._("The language has been changed to {language}.").format(language=language)