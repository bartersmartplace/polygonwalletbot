from typing import Union
from aiogram.types import (
    Message,
    CallbackQuery,

)
from aiogram.enums import ParseMode
from aiogram import Bot
from tg_bot.views import MessageSender
from tg_bot.templates import ButtonPresenter


class BaseView:
    def __init__(self, bot: Bot, bot_id: int, button_presenter: ButtonPresenter):
        self.__bot = bot
        self.__message_sender = MessageSender(bot_id=bot_id)
        self.__button_presenter = button_presenter

    async def send_message_by_id(self, chat_id: int, text: str):
        await self.__bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


    async def send_error_message(self, event: Union[Message, CallbackQuery], text: str):
        await self.__message_sender.send_or_edit(event=event, text=text)
    

    async def send_message(self, event: Union[Message, CallbackQuery], text: str):
        message = await self.__message_sender.send_or_edit(
                event=event,
                text=text,
            )
        return message