from typing import Union
from aiogram.types import (
    Message,
    CallbackQuery,

)
from aiogram.enums import ParseMode
from aiogram import Bot
from tg_bot.views import MessageSender
from tg_bot.keyboards import SwapKeyboard
from tg_bot.templates import ButtonPresenter


class SwapView:
    def __init__(self, bot: Bot, bot_id: int, button_presenter: ButtonPresenter):
        self.__bot = bot
        self.__message_sender = MessageSender(bot_id=bot_id)
        self.__button_presenter = button_presenter


    async def send_brub_manual(self, chat_id: int, text: str):
        кeyboard = SwapKeyboard(self.__button_presenter)
        await self.__bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=кeyboard.brub_keyboard(),
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
            )


    async def send_swap_parameters_message(self, event: Union[Message, CallbackQuery], text: str):
        кeyboard = SwapKeyboard(self.__button_presenter)
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            disable_web_page_preview=True,
            reply_markup=кeyboard.swap_parameters_keyboard(),
        )