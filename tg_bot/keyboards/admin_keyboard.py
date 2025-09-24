from aiogram.types import InlineKeyboardButton
from .inline_generator import gen_inline_markup
from tg_bot.templates.buttons import text, callbacks
from tg_bot.templates import ButtonPresenter


class AdminKeyboard:
    MAX_ROW_LENGTH = 2

    def __init__(self, button_presenter: ButtonPresenter) -> None:
        self.__buttons = button_presenter


    def main_admin_keyboard(self):
        buttons_list = [
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.USER_COUNT_TEXT),
                    callback_data=callbacks.BroadcastingCallbackData(option=text.USER_COUNT_TEXT).pack(),
                    resize_keyboard = True),

                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.MESSAGE_BROADCASTING_TEXT),
                    callback_data=callbacks.BroadcastingCallbackData(option=text.MESSAGE_BROADCASTING_TEXT).pack(),
                    resize_keyboard = True)
                                        
            ]
        main_admin_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return main_admin_keyboard


    def broadcasting_manage_keyboard(self):
        buttons_list = [
                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.ADD_BUTTON_TEXT),
                    callback_data=callbacks.AddButtonCallbackData(action=text.ADD_BUTTON_TEXT).pack(),
                    resize_keyboard = True),

                InlineKeyboardButton(
                    text=self.__buttons.get_button_text(text.SEND_ADMIN_MESSAGE_TEXT),
                    callback_data=callbacks.SendAdminMessageCallbackData(action=text.SEND_ADMIN_MESSAGE_TEXT).pack(),
                    resize_keyboard = True),
            ]
        broadcasting_manage_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)

        return broadcasting_manage_keyboard
    

    def broadcasting_message_keyboard(self, button_list, buttons_link):
        buttons_list = []
        for button_text, button_link in zip(button_list, buttons_link):
            button = InlineKeyboardButton(
                text=button_text,
                url=button_link
            )
            buttons_list.append(button)
        broadcasting_message_keyboard = gen_inline_markup(buttons_list, self.MAX_ROW_LENGTH)
        return broadcasting_message_keyboard