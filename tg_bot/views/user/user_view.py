from typing import Union
from aiogram.types import (
    Message,
    CallbackQuery,

)
from aiogram.enums import ParseMode
from aiogram import Bot
from tg_bot.views import MessageSender
from tg_bot.keyboards import UserKeyboard
from tg_bot.templates import ButtonPresenter


class UserView:
    def __init__(self, bot: Bot, bot_id: int, button_presenter: ButtonPresenter):
        self.__bot = bot
        self.__message_sender = MessageSender(bot_id=bot_id)
        self.__button_presenter = button_presenter
    

    async def send_address_list_message(self, event: Union[Message, CallbackQuery], text: str)  -> None:
        кeyboard = UserKeyboard(self.__button_presenter)
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=кeyboard.add_new_address_keyboard()
            )
    

    async def send_address_update_message(self, event: Union[Message, CallbackQuery], text: str)  -> None:
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            parse_mode=ParseMode.MARKDOWN
            )
    

    async def send_active_address(self, event: Union[Message, CallbackQuery], text: str)  -> None:
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            parse_mode=ParseMode.MARKDOWN
            )
    

    async def send_referal_link(self, chat_id: int, text: str):
        await self.__bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN)

    
    async def send_choose_language_message(self, event: Union[Message, CallbackQuery], text: str)  -> None:
        кeyboard = UserKeyboard(self.__button_presenter)
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            reply_markup=кeyboard.language_keyboard(),
            parse_mode=ParseMode.MARKDOWN
            )