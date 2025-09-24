from aiogram import Bot
from aiogram.enums import ParseMode
from tg_bot.views import MessageSender
from tg_bot.keyboards import AdminKeyboard
from tg_bot.templates import ButtonPresenter


class AdminView:
    def __init__(self, bot: Bot, bot_id: int, button_presenter: ButtonPresenter):
        self.__bot = bot
        self.__message_sender = MessageSender(bot_id=bot_id)
        self.__button_presenter = button_presenter


    async def send_admin_menu_message(self, chat_id: int, text: str):
        кeyboard = AdminKeyboard(self.__button_presenter)
        await self.__bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=кeyboard.main_admin_keyboard()
            )


    async def send_preview_message(self, chat_id: int,
                                   text: str,
                                   button_list = None,
                                   buttons_link = None):
        кeyboard = AdminKeyboard(self.__button_presenter)
        await self.__bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=кeyboard.broadcasting_message_keyboard(button_list, buttons_link),
            parse_mode=ParseMode.MARKDOWN
            )


    async def send_add_button_message(self, chat_id: int, text: str):
        кeyboard = AdminKeyboard(self.__button_presenter)
        await self.__bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=кeyboard.broadcasting_manage_keyboard()
            )