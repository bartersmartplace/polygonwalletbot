from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from domain.common.errors import AppError
from .user_router import user_router
from tg_bot.controllers import UserController
from tg_bot.presenters.user import UserPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.user import UserView
from tg_bot.views.base import BaseView
from tg_bot.templates.buttons import text, callbacks



@user_router.callback_query(callbacks.DepositCallbackData.filter(F.action == text.DEPOSIT_TEXT))
async def get_active_address(
    query: CallbackQuery,
    state: FSMContext,
    session,
    user_presenter: UserPresenter,
    user_view: UserView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await query.answer()
    telegram_id = query.from_user.id
    try:
        user_controller = UserController(session)
        active_address = await user_controller.get_active_address(telegram_id)
        get_active_address_message = user_presenter.get_active_address_message(active_address)
        await user_view.send_address_update_message(query, get_active_address_message)
        
    except AppError as error:
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(query, error_message)
    
    finally:
        await state.clear()