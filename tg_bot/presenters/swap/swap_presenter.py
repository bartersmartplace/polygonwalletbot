from aiogram.utils.markdown import hlink
from app.application.dto import TradeDTO
from tg_bot.presenters import format_number_value
from tg_bot.localization import _


class SwapPresenter:
    def __init__(self, language: str = "en"):
        self._ = lambda text: _(text, locale=language)


    def get_brub_manual(self) -> str:
        return self._(
            "Barter RUB [{link}] is a token linked to the value of the ruble.\n\n"
            "Get RUB in the ratio of 1:1 to the ruble to buy tokenized assets,\n"
            "goods and services around the world, NFT, and other tokens.\n\n"
            "Getting a BRUB is simple:\n\n"
            "1. Click the Get BRUB button and select the bank to transfer via SBP,\n"
            "2. Enter the amount for tokenization in the bank's application and confirm the transfer,\n"
            "3. Send the transfer receipt and the wallet address for crediting tokens to @dprolix.\n\n"
        ).format(link=hlink("BRUB", "https://polygonscan.com/token/0x6E29221f7452D9F86B8E9b6b4de911ABab8E38BB"))


    def get_return_brub_message(self) -> str:
        return self._("You can return from 100000 BRUB with a 7% commission. Send the wallet address with BRUB and the amount to @dprolix.")


    def get_swap_manual(self) -> str:
        return self._(
            "To make a quick token swap, enter a command like "
            '"swap [token amount for sale] [token ticker for sale] [token ticker for buy]":\n\n'
            "swap 10 USDT BRTR\n\n"
            "Liquidity provided by Uniswap"
        )


    def get_swap_parameters_message(self, trade: TradeDTO) -> str:
        amount_to_sell = format_number_value(trade.amount_to_sell / 10 ** trade.sell_token.decimal, 4)
        amount_to_buy = format_number_value(trade.amount_to_buy / 10 ** trade.buy_token.decimal, 4)

        return self._(
            "Sell: {amount_to_sell} {sell_symbol}\n"
            "Buy: {amount_to_buy} {buy_symbol}\n"
            "Slippage: 1%"
        ).format(
            amount_to_sell=amount_to_sell,
            sell_symbol=trade.sell_token.symbol,
            amount_to_buy=amount_to_buy,
            buy_symbol=trade.buy_token.symbol,
        )


    def get_ask_password_message(self) -> str:
        return self._("Enter the password from the currently active wallet to perform the exchange operation")


    def get_cancel_trade_operation_message(self) -> str:
        return self._("The exchange operation has been cancelled")