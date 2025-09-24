from typing import Union
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram import Bot
from tg_bot.views import MessageSender
from tg_bot.keyboards import TokenKeyboard
from tg_bot.templates import ButtonPresenter


class TokenView:
    def __init__(self, bot: Bot, bot_id: int, button_presenter: ButtonPresenter):
        self.__bot = bot
        self.__message_sender = MessageSender(bot_id=bot_id)
        self.__button_presenter = button_presenter


    async def send_base_stake_info_message(self, chat_id: int, text: str):
        кeyboard = TokenKeyboard(self.__button_presenter)
        await self.__bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=кeyboard.stake_keyboard(),
            disable_web_page_preview=True,
            )


    async def send_stake_tx_message(self, event: Union[Message, CallbackQuery], text: str):
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML
            )
    
    
    async def send_message_to_adding_ERC20(self, event: Union[Message, CallbackQuery], text: str):
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            )
    

    async def send_ask_to_add_ERC20(self, event: Union[Message, CallbackQuery], text: str):
        кeyboard = TokenKeyboard(self.__button_presenter)
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            reply_markup=кeyboard.ask_to_add_token_keyboard(),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
            )
    

    async def send_choose_way_to_add_token_message(self, event: Union[Message, CallbackQuery], text: str):
        кeyboard = TokenKeyboard(self.__button_presenter)
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            reply_markup=кeyboard.add_token_keyboard(),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
            )
    

    async def send_paid_message(self, event: Union[Message, CallbackQuery], text: str):
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
            )