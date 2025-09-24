from typing import List
from app.application.dto import TokenDTO
from aiogram.types import InlineKeyboardButton
from .inline_generator import gen_inline_markup
from tg_bot.templates import ButtonPresenter
from tg_bot.templates.buttons import text, callbacks


class AddressKeyboard:
    MAX_ROW_LENGTH = 2


    def __init__(self, button_presenter: ButtonPresenter) -> None:
        self.__buttons = button_presenter

    
    def pay_for_new_address_keyboard(self):
        buttons_list = [
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.PAY_TEXT),
                    callback_data=callbacks.PaymentForNewAddressCallbackData(
                        action=text.PAY_TEXT
                        ).pack(),
                    resize_keyboard=True)
            ]
        pay_for_new_address_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return pay_for_new_address_keyboard
    
    
    def address_keyboard(self):
        buttons_list = [
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.DEPOSIT_TEXT),
                    callback_data=callbacks.DepositCallbackData(action=text.DEPOSIT_TEXT).pack(),
                    resize_keyboard=True),
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.SEND_TEXT),
                    callback_data=callbacks.SendCallbackData(action=text.SEND_TEXT, token="").pack(),
                    resize_keyboard=True),
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.ADD_TOKEN),
                    callback_data=callbacks.PaymentForERC20CallbackData(action=text.ADD_TOKEN, token="").pack(),
                    resize_keyboard=True)
            ]
        address_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return address_keyboard

    
    def sendable_tokens_keyboard(self, tokens: List[TokenDTO]):
        buttons_list = [
            InlineKeyboardButton(
                text=token.symbol,
                callback_data=callbacks.SendCallbackData(action=text.SEND_TEXT, 
                                                         token=token.symbol).pack(),
                resize_keyboard=True
            )
            for token in tokens
        ]
        buttons_list.append(InlineKeyboardButton(
            text=self.__buttons.get_button_text(text.BACK_SYMBOL),
            callback_data=callbacks.BalanceCallbackData(action=text.BACK_SYMBOL).pack(),
            resize_keyboard = True))
        
        if len(buttons_list) < 6:
            row_lengt = 1
        else:
            row_lengt = self.MAX_ROW_LENGTH
        sendable_tokens_keyboard = gen_inline_markup(buttons_list, row_lengt)

        return sendable_tokens_keyboard

    
    def recipient_cancel_keyboard(self):
        buttons_list = [
            InlineKeyboardButton(
                text=self.__buttons.get_button_text(text.CANCEL_TEXT),
                callback_data=callbacks.SendCallbackData(action=text.SEND_TEXT, token="").pack(),
                resize_keyboard = True)
        ]
        recipient_cancel_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return recipient_cancel_keyboard

    
    def confirmation_tx_keyboard(self):
        buttons_list = [
            InlineKeyboardButton(
                text=self.__buttons.get_button_text(text.CONFIRM_TEXT),
                callback_data=callbacks.ConfirmCallbackData(action=text.CONFIRM_TEXT).pack(),
                resize_keyboard = True),
            InlineKeyboardButton(
                text=self.__buttons.get_button_text(text.CANCEL_TEXT),
                callback_data=callbacks.SendCallbackData(action=text.SEND_TEXT, token="").pack(),
                resize_keyboard = True)
        ]
        confirmation_tx_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return confirmation_tx_keyboard