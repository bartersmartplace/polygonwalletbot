from typing import Union
from aiogram.types import (
    Message,
    CallbackQuery,

)
from aiogram.enums import ParseMode
from aiogram import Bot
from tg_bot.views import MessageSender
from tg_bot.keyboards import AddressKeyboard
from tg_bot.templates import ButtonPresenter


class AddressView:
    def __init__(self, bot: Bot, bot_id: int, button_presenter: ButtonPresenter):
        self.__bot = bot
        self.__message_sender = MessageSender(bot_id=bot_id)
        self.__button_presenter = button_presenter


    async def send_address_generation_message(self, chat_id: int, text: str):
        await self.__bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN,
            )


    async def send_message_to_start_generating_new_address(self, chat_id: int, text: str):
        кeyboard = AddressKeyboard(self.__button_presenter)
        await self.__bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=кeyboard.pay_for_new_address_keyboard()
            )


    async def send_message_of_successful_paying(self, event: Union[Message, CallbackQuery], text: str):
         await self.__message_sender.send_or_edit(
            event=event,
            text=text, 
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
            )


    async def sent_transaction_message(self, event: Union[Message, CallbackQuery], text: str):
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
            )


    async def send_balance_message(self, event: Union[Message, CallbackQuery], text: str):
        кeyboard = AddressKeyboard(self.__button_presenter)
        await self.__message_sender.send_or_edit(
            event=event,
            text=text, 
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=кeyboard.address_keyboard(),
            disable_web_page_preview=True
            )
    

    async def send_tokens_to_send_message(self, event: Union[Message, CallbackQuery], text: str, tokens):
         кeyboard = AddressKeyboard(self.__button_presenter)
         await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            reply_markup=кeyboard.sendable_tokens_keyboard(tokens),
            disable_web_page_preview=True
            )
    

    async def send_ask_recipient_message(self, event: Union[Message, CallbackQuery], text: str):
        кeyboard = AddressKeyboard(self.__button_presenter)
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            disable_web_page_preview=True,
            reply_markup=кeyboard.recipient_cancel_keyboard(),
        )
    

    async def send_ask_tx_confirmation(self, event: Union[Message, CallbackQuery], text: str):
        кeyboard = AddressKeyboard(self.__button_presenter)
        await self.__message_sender.send_or_edit(
            event=event,
            text=text,
            disable_web_page_preview=True,
            reply_markup=кeyboard.confirmation_tx_keyboard(),
        )