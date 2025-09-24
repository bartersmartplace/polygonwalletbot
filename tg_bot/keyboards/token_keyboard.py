from aiogram.types import InlineKeyboardButton
from .inline_generator import gen_inline_markup
from tg_bot.templates.buttons import text, callbacks
from tg_bot.templates import ButtonPresenter


class TokenKeyboard:
    MAX_ROW_LENGTH = 2


    def __init__(self, button_presenter: ButtonPresenter) -> None:
        self.__buttons = button_presenter


    def stake_keyboard(self):
        buttons_list = [
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.ADD_TEXT),
                    callback_data=callbacks.StakeCallbackData(action=text.ADD_TEXT).pack(),
                    resize_keyboard = True),

                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.REMOVE_TEXT),
                    callback_data=callbacks.StakeCallbackData(action=text.REMOVE_TEXT).pack(),
                    resize_keyboard = True)
                                        
            ]
        stake_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return stake_keyboard
    
    def ask_to_add_token_keyboard(self):
        buttons_list = [
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.ADD_TEXT),
                    callback_data=callbacks.AddERC20(
                        action=text.ADD_TEXT
                        ).pack(),
                    resize_keyboard=True),

                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.BACK_TEXT),
                    callback_data=callbacks.PaymentForERC20CallbackData(
                        action=text.ADD_TOKEN
                        ).pack(),
                    resize_keyboard=True)
            ]
        ask_to_add_token_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return ask_to_add_token_keyboard
    

    def add_token_keyboard(self):
        buttons_list = [
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.ONLY_FOR_ME),
                    callback_data=callbacks.AddERC20(
                        action=text.ONLY_FOR_ME
                        ).pack(),
                    resize_keyboard=True),

                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.PAY_FOR_LISTING),
                    callback_data=callbacks.AddERC20(
                        action=text.PAY_FOR_LISTING
                        ).pack(),
                    resize_keyboard=True)
            ]
        ask_to_add_token_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)
        print(callbacks.AddERC20(
                        action=text.ONLY_FOR_ME
                        ).pack(),)
        return ask_to_add_token_keyboard
        

    def pay_for_add_ERC20_keyboard(self):
        buttons_list = [
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.PAY_TEXT),
                    callback_data=callbacks.PaymentForERC20CallbackData(
                        action=text.PAY_TEXT
                        ).pack(),
                    resize_keyboard=True)
            ]
        pay_for_ERC20_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return pay_for_ERC20_keyboard