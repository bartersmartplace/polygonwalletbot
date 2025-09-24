from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery
from infrastructure.database import get_async_session
from tg_bot.controllers import UserController
from tg_bot.presenters.admin import AdminPresenter
from tg_bot.views.admin import AdminView
from tg_bot.presenters.base import BasePresenter
from tg_bot.templates import ButtonPresenter
from tg_bot.views.base import BaseView


class AdminMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot, bot_id: int):
        super().__init__()
        self.bot = bot
        self.bot_id = bot_id


    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        telegram_id = event.from_user.id
        async_session_generator = get_async_session()
        async_session = await async_session_generator.__anext__()
        async with async_session as session:
            user_controller = UserController(session)
            user = await user_controller.get_user_by_telegram_id(telegram_id)
            user_language = user.language
            is_admin = user.is_admin
            if not is_admin:
                return

            button_presenter = ButtonPresenter(language=user_language)
            data["session"] = session
            data["admin_presenter"] = AdminPresenter(language=user_language)
            data["admin_view"] = AdminView(bot=self.bot, bot_id=self.bot_id, button_presenter=button_presenter)
            data["base_presenter"] = BasePresenter(language=user_language)
            data["base_view"] = BaseView(bot=self.bot, bot_id=self.bot_id, button_presenter=button_presenter)

            return await handler(event, data)