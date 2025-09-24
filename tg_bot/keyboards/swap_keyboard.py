from aiogram.types import InlineKeyboardButton
from .inline_generator import gen_inline_markup
from tg_bot.templates.buttons import text, callbacks
from tg_bot.templates import ButtonPresenter


class SwapKeyboard:
    MAX_ROW_LENGTH = 2


    def __init__(self, button_presenter: ButtonPresenter) -> None:
        self.__buttons = button_presenter


    def brub_keyboard(self):
        buttons_list = [
            InlineKeyboardButton(
                text=self.__buttons.get_button_text(text.GET_BRUB_TEXT),
                url="https://qr.nspk.ru/BS1A0027K1JB2RU59BCA05OBBJPMIP2T?type=01&bank=100000000004&crc=A7E6",
                callback_data=callbacks.BrubCallbackData(action=text.GET_BRUB_TEXT).pack(),
                resize_keyboard = True),

            InlineKeyboardButton(
                text=self.__buttons.get_button_text(text.RETURN_BRUB_TEXT),
                callback_data=callbacks.BrubCallbackData(action=text.RETURN_BRUB_TEXT).pack(),
                resize_keyboard = True)
        ]
        brub_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return brub_keyboard
    

    
    def swap_parameters_keyboard(self):
        buttons_list = [
            InlineKeyboardButton(
                text=self.__buttons.get_button_text(text.CONFIRM_TEXT),
                callback_data=callbacks.SwapCallbackData(action=text.CONFIRM_TEXT).pack(),
                resize_keyboard = True),

            InlineKeyboardButton(
                text=self.__buttons.get_button_text(text.CANCEL_TEXT),
                callback_data=callbacks.SwapCallbackData(action=text.CANCEL_TEXT).pack(),
                resize_keyboard = True)
                                    
        ]
        swap_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return swap_keyboard