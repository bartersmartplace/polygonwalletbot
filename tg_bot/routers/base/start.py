from aiogram.filters import CommandStart
from aiogram.types import  Message
from aiogram.fsm.context import FSMContext
from domain.common.errors import AppError
from .base_router import base_router
from tg_bot.controllers import UserController
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.base import BaseView

@base_router.message(CommandStart())
async def start(
    message: Message,
    state: FSMContext,
    session,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    try:
        await state.clear()
        telegram_id = message.from_user.id
        name = message.from_user.first_name
        username = message.from_user.username

        referrer_id = _extract_referrer_id(message.text)
        start_message = base_presenter.get_start_message()
        await base_view.send_message_by_id(chat_id=telegram_id, text=start_message)

        user_controller = UserController(session)
        await user_controller.create_user(
            telegram_id=telegram_id,
            tg_name=name,
            tg_username=username,
            referrer_id=referrer_id,
        )

    except AppError as error:
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)


def _extract_referrer_id(command_text: str) -> int | None:
    parts = command_text.split(maxsplit=1)
    if len(parts) > 1 and parts[1].isdigit():
        return int(parts[1])
    
    return None