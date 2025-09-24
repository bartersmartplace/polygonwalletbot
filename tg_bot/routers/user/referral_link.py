from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.config import  PAY_TOKEN_SYMBOL_TO_GENERATE_NEW_ADDRESS, PAY_TOKEN_DECIMALS
from .user_router import user_router
from tg_bot.controllers import UserController
from tg_bot.presenters.user import UserPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.user import UserView


@user_router.message(Command("referral"))
async def referral_link(
    message: Message,
    state: FSMContext,
    session,
    user_presenter: UserPresenter,
    user_view: UserView,
    base_presenter: BasePresenter,
    ):
    await state.clear()
    bot = await message.bot.get_me()
    telegram_id = message.from_user.id
    user_controller = UserController(session)
    ref_data = await user_controller.get_ref_data(telegram_id)
    referral_message = user_presenter.get_referal_link_message(bot.username, telegram_id, ref_data,
                                                               PAY_TOKEN_DECIMALS, PAY_TOKEN_SYMBOL_TO_GENERATE_NEW_ADDRESS)
    await user_view.send_referal_link(chat_id=telegram_id, text=referral_message)