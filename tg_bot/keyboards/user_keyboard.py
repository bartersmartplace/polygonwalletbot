from aiogram.types import InlineKeyboardButton
from .inline_generator import gen_inline_markup
from tg_bot.templates.buttons import text, callbacks
from tg_bot.templates import ButtonPresenter


class UserKeyboard:
    MAX_ROW_LENGTH = 2
    
    
    def __init__(self, button_presenter: ButtonPresenter) -> None:
        self.__buttons = button_presenter

    
    def add_new_address_keyboard(self):
        buttons_list = [
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.ADD_NEW_ADDRESS_TEXT),
                    callback_data=callbacks.NewAddressCallbackData(action=text.ADD_NEW_ADDRESS_TEXT).pack(),
                    resize_keyboard=True)
            ]
        add_address_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return add_address_keyboard

    
    def language_keyboard(self):
        buttons_list = [
            InlineKeyboardButton(
                text=self.__buttons.get_button_text(text.ENG_TEXT),
                callback_data=callbacks.LanguageCallbackData(language=text.ENG_TEXT).pack(),
                resize_keyboard = True),

            InlineKeyboardButton(
                text=self.__buttons.get_button_text(text.RUS_TEXT),
                callback_data=callbacks.LanguageCallbackData(language=text.RUS_TEXT).pack(),
                resize_keyboard = True),
                                    
        ]
        language_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return language_keyboard