from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery
from app.application.dto import UserDTO
from infrastructure.database import get_async_session
from tg_bot.controllers import UserController
from tg_bot.presenters.token import TokenPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.templates import ButtonPresenter
from tg_bot.views.token import TokenView
from tg_bot.views.base import BaseView

class TokenMiddleware(BaseMiddleware):
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
            user: UserDTO = await user_controller.get_user_by_telegram_id(telegram_id)
            user_language = user.language if user else "en"
            button_presenter = ButtonPresenter(language=user_language)
            data["user"] = user
            data["session"] = session
            data["token_presenter"] = TokenPresenter(language=user_language)
            data["token_view"] = TokenView(bot=self.bot, bot_id=self.bot_id, button_presenter=button_presenter)
            data["base_presenter"] = BasePresenter(language=user_language)
            data["base_view"] = BaseView(bot=self.bot, bot_id=self.bot_id, button_presenter=button_presenter)

            return await handler(event, data)