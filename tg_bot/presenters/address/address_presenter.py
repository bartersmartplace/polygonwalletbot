from decimal import Decimal
from aiogram.utils.markdown import hlink, link
from app.application.dto import BalanceDTO
from tg_bot.presenters import format_number_value
from tg_bot.localization import _


class AddressPresenter:
    def __init__(self, language: str):
        self._ = lambda text: _(text, locale=language)


    def get_generate_address_information_message(self, network_name: str = "Polygon") -> str:
        return self._(
            "Enter a new password for your new address in the {network_name} blockchain.\n"
            "The password must be at least 8 characters long, contain a special character and a capital letter.\n\n"
            "This password will be requested to sign transactions and send funds from the wallet.\n"
            "Don't tell anyone about it and keep it a secret. Our service does not store users' passwords,\n"
            "and if you lose it, you will lose access to your wallet and all funds.\n\n"
            "Save your password on paper as well. Be safe every day."
        ).format(network_name=network_name)


    def get_successful_address_generation_message(self, address: str):
        return self._(
            "Address: `{address}` successfully created.\n"
            "Please keep your password a secret and store it securely.\n"
            "You can send and receive tokens using this address."
        ).format(address=address)


    def get_generate_new_address_message(self, pay_token_symbol: str, pay_token_decimals: int, price: int):
        return self._(
            "Generating an additional address costs {price} {symbol}."
        ).format(price=format_number_value(price / 10 ** pay_token_decimals, 0), symbol=pay_token_symbol)


    def get_password_entering_for_new_address_message(self):
        return self._("Enter the password for the wallet from which the funds will be debited.")


    def get_successful_paying_for_new_address_message(self, pay_token_symbol: str, pay_token_decimals: int, price: int, tx_hash: str):
        tx_hash_url = f"https://polygonscan.com/tx/{tx_hash}"
        return self._(
            "You paid {amount} {symbol} for a new address.\n"
            "{transaction_hash}"
        ).format(
            amount=format_number_value(price / 10 ** pay_token_decimals, 0),
            symbol=pay_token_symbol,
            transaction_hash=hlink(self._("Transaction hash"), tx_hash_url),
        )


    def get_tx_message(self, sent_amount: int, sent_token_symbol: str, recipient_address: str, tx_hash: str):
        tx_hash_url = f"https://polygonscan.com/tx/{tx_hash}"
        return self._(
            "You sent {amount} {symbol} to {recipient}.\n"
            "{transaction_hash}"
        ).format(
            amount=format_number_value(sent_amount),
            symbol=sent_token_symbol.upper(),
            recipient=recipient_address,
            transaction_hash=hlink(self._("Transaction hash"), tx_hash_url),
        )


    def get_balances_message(self, balance_information: BalanceDTO) -> str:
        message = f"`{balance_information.address}`\n\n"

        for token, balance in balance_information.tokens:
            actual_balance = Decimal(balance) / Decimal(10 ** token.decimal)
            token_url = (
                f"https://polygonscan.com/token/{token.address}"
                if token.address
                else "https://polygonscan.com"
            )
            formatted_balance = format_number_value(actual_balance)
            message += _("{symbol} - {balance}").format(
                symbol=link(token.symbol, token_url), balance=formatted_balance
            ) + "\n"

        return message


    def get_choose_token_message(self):
        return self._("Which asset will be sent?")


    def get_enter_recipient_message(self, network_name: str = "Polygon"):
        return self._(
            "Enter the recipient's {network_name} chain wallet address or @username of the user in Telegram."
        ).format(network_name=network_name)


    def get_enter_amount_message(self, token_balance: BalanceDTO):
        token, balance = token_balance.tokens[0]
        actual_balance = Decimal(balance) / Decimal(10 ** token.decimal)
        formatted_balance = format_number_value(actual_balance)
        return self._(
            "Balance: {balance} {symbol}\n"
            "Enter the amount to send."
        ).format(balance=formatted_balance, symbol=token.symbol)


    def get_submit_tx_message(self, amount: float, token_symbol: str, recipient: str):
        return self._(
            "Submit transaction:\n\n"
            "Value: {amount} {symbol}\n"
            "Recipient: {recipient}"
        ).format(amount=amount, symbol=token_symbol, recipient=recipient)


    def get_ask_password_entering_message(self):
        return self._("Enter the password for this wallet to confirm the operation.")
    

    def get_active_address_is_not_set_message(self):
        return self._("The active address is not set, set it with the /addresses command.")

