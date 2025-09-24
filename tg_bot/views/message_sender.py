from typing import Optional, Union
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
)
from aiogram.enums import ParseMode


class MessageSender:
    def __init__(self, bot_id: int):
        self.bot_id = bot_id

    async def send_or_edit(
        self,
        event: Union[Message, CallbackQuery],
        text: str,
        parse_mode: Optional[ParseMode] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_markup: Optional[
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
        ] = None,
        show_alert: bool = False,
        **kwargs,
    ) -> Union[Message, bool]:
        """
        Handles sending or editing messages depending on the event type and bot ID.
        - For `Message` events, either edits the message if the bot sent it, or replies otherwise.
        - For `CallbackQuery` events, either edits the associated message or answers the callback.

        :param event: Event object (`Message` or `CallbackQuery`)
        :param text: The text to send/edit
        :param parse_mode: Text parse mode (e.g., Markdown, HTML)
        :param disable_web_page_preview: Disable web previews for URLs in the text
        :param disable_notification: Send message silently (no notification)
        :param reply_markup: Markup for inline keyboards
        :param show_alert: Whether to show an alert for `CallbackQuery`
        :param kwargs: Additional arguments for `edit_text` or `answer` methods
        :return: The result of the send/edit operation
        """
        if isinstance(event, Message):
            return await self._handle_message(
                event=event,
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
                reply_markup=reply_markup,
                **kwargs,
            )
        elif isinstance(event, CallbackQuery):
            return await self._handle_callback_query(
                callback_query=event,
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                disable_web_page_preview=disable_web_page_preview,
                show_alert=show_alert,
                **kwargs,
            )
        else:
            raise TypeError(f"Unsupported event type: {type(event)}")

    async def _handle_message(
        self,
        event: Message,
        text: str,
        parse_mode: Optional[ParseMode],
        disable_web_page_preview: Optional[bool],
        disable_notification: Optional[bool],
        reply_markup: Optional[
            InlineKeyboardMarkup
            | ReplyKeyboardMarkup
            | ReplyKeyboardRemove
            | ForceReply
        ],
        **kwargs,
    ) -> Message:
        """
        Handle `Message` events and decide whether to edit or reply.
        """
        if event.from_user.id == self.bot_id:
            return await event.edit_text(
                text=text,
                parse_mode=parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                reply_markup=reply_markup,
                **kwargs,
            )
        return await event.answer(
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
            **kwargs,
        )

    async def _handle_callback_query(
        self,
        callback_query: CallbackQuery,
        text: str,
        parse_mode: Optional[ParseMode],
        reply_markup: Optional[InlineKeyboardMarkup],
        show_alert: bool,
        **kwargs,
    ) -> Union[bool, Message]:
        """
        Handle `CallbackQuery` events and decide whether to edit or answer the query.
        """
        if callback_query.message and callback_query.from_user.id == self.bot_id:
            return await callback_query.message.edit_text(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup,
                **kwargs,
            )
        return await callback_query.message.answer(
            text=text,
            show_alert=show_alert,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            **kwargs,
        )
