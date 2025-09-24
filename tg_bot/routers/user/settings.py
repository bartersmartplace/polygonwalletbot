from aiogram.types import  Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from .user_router import user_router
from tg_bot.presenters.user import UserPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.user import UserView


@user_router.message(Command("settings"))
async def settings(
    message: Message,
    state: FSMContext,
    session,
    user_presenter: UserPresenter,
    user_view: UserView,
    base_presenter: BasePresenter,
    ):
    await state.clear()
    choose_language_message = user_presenter.get_choose_language_message()
    await user_view.send_choose_language_message(message, choose_language_message)
