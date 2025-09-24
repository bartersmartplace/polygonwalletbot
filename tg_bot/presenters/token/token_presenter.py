from typing import List
from decimal import Decimal
from aiogram.utils.markdown import hlink
from app.application.dto import  BalanceDTO, TokenDTO
from tg_bot.presenters import format_number_value
from tg_bot.localization import _


class TokenPresenter:
    def __init__(self, language: str = "en"):
        self._ = lambda text: _(text, locale=language)


    def get_stake_information(self, BRTR: BalanceDTO, stBRTR: BalanceDTO, stakers_count: int, totalValueLocked: int) -> str:
        brtr_balance = format_number_value(Decimal(BRTR.tokens[0][1]) / Decimal(10 ** BRTR.tokens[0][0].decimal))
        st_brtr_balance = format_number_value(Decimal(stBRTR.tokens[0][1]) / Decimal(10 ** stBRTR.tokens[0][0].decimal))

        return self._(
            "Staked BRTR: {st_brtr_balance}\n"
            "BRTR balance: {brtr_balance}\n\n"
            "Stakers: {stakers_count}\n\n"
            "TVL: {tvl:,}\n"
            "Add to stake from 100 BRTR."
        ).format(st_brtr_balance=st_brtr_balance, brtr_balance=brtr_balance, stakers_count=stakers_count, tvl=totalValueLocked)

    def get_paid_message(
            self,
            tx_hash,
            pay_token_symbol: str,
            pay_token_decimals: int,
            price: int
            ):
        return self._(
            "You paid {price} {symbol} to add token\n" + \
            "{hash_link}"
        ).format(
            hash_link=hlink(self._("Transaction hash"), f"https://polygonscan.com/tx/{tx_hash}"),
            price=format_number_value(price / 10 ** pay_token_decimals, 0),
            symbol=pay_token_symbol,
            )

    def get_start_brtr_stake_message(self, tx_hash: str, amount: float) -> str:
        return self._(
            "+{amount} BRTR added to staking\n{hash_link}"
        ).format(amount=format_number_value(amount), hash_link=hlink(self._("Transaction hash"), f"https://polygonscan.com/tx/{tx_hash}"))


    def get_stop_brtr_stake_message(self, tx_hash: str, amount: float) -> str:
        return self._(
            "-{amount} BRTR removed from staking.\n{hash_link}"
        ).format(amount=format_number_value(amount), hash_link=hlink(self._("Transaction hash"), f"https://polygonscan.com/tx/{tx_hash}"))


    def ask_how_much_brtr_add_to_stake(self) -> str:
        return self._("How much BRTR to add?")


    def ask_how_much_brtr_to_remove_from_stake(self) -> str:
        return self._("How much BRTR to remove?")


    def ask_to_enter_ERC20_contractr(self) -> str:
        return self._("Enter token’s smart contract address to add to the wallet")


    def get_ask_password_entering_message(self) -> str:
        return self._("Enter the password from this address to confirm the operation")
    

    def get_ask_to_add_erc20(self, token: TokenDTO):
        return self._(
            "Do you want to add {symbol} ?"
            ).format(symbol=hlink(self._(token.symbol), f"https://polygonscan.com/token/{token.address}"))
    

    def get_choose_way_to_add_token_message(
            self,
            new_token: TokenDTO,
            tokens: List[TokenDTO],
            tokens_limit: int,
            pay_token_symbol: str,
            pay_token_decimals: int,
            price_to_add_erc20_to_user: int,
            pay_token_symbol_to_add_erc20_to_everyone,
            pay_token_decimals_to_add_erc20_to_everyone,
            price_to_add_erc20_to_everyone
            ):
        message = ""
        price_to_add_erc20_to_user = format_number_value(
            price_to_add_erc20_to_user / 10 ** pay_token_decimals, 0
        )
        price_to_add_erc20_to_everyone = format_number_value(
            price_to_add_erc20_to_everyone / 10 ** pay_token_decimals_to_add_erc20_to_everyone, 0
        )
        if len(tokens) < tokens_limit:
            message = self._(
                "The token {new_token_symbol} will be added for free just for you and recipients.\n" + \
                "If you want to list a token to the /assets section for everyone users, it costs {price_to_add_erc20_to_everyone} {pay_token_symbol}."
            ).format(
                new_token_symbol=hlink(self._(new_token.symbol), f"https://polygonscan.com/token/{new_token.address}"),
                price_to_add_erc20_to_everyone = f"{price_to_add_erc20_to_everyone:,}".replace(",", " "),
                pay_token_symbol=pay_token_symbol,
                )

        else:
            message = self._(
                "The token {new_token_symbol} will be added for {price_to_add_erc20_to_user} {pay_token_symbol} just for you and recipients.\n" + \
                "If you want to list a token to the /assets section for everyone users, it costs {price_to_add_erc20_to_everyone} {pay_token_symbol}."
            ).format(
                new_token_symbol=hlink(self._(new_token.symbol), f"https://polygonscan.com/token/{new_token.address}"),
                price_to_add_erc20_to_user=price_to_add_erc20_to_user,
                price_to_add_erc20_to_everyone = f"{price_to_add_erc20_to_everyone:,}".replace(",", " "),
                pay_token_symbol=pay_token_symbol_to_add_erc20_to_everyone,
                )

        return message
    

    def get_new_token_added_message(self):
        return self._("You added new token")