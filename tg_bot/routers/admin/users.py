from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from tg_bot.controllers import AdminController
from tg_bot.presenters.admin import AdminPresenter
from tg_bot.views.admin import AdminView
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.base import BaseView
from .admin_router import admin_router
from tg_bot.templates.buttons import text, callbacks


@admin_router.callback_query(callbacks.BroadcastingCallbackData.filter(F.option == text.USER_COUNT_TEXT))
async def user_count(
    query: CallbackQuery,
    state: FSMContext,
    session,
    admin_presenter: AdminPresenter,
    admin_view: AdminView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await query.answer()
    await state.clear()
    admin_controller = AdminController(session)
    users_count = await admin_controller.get_user_count()
    user_count_message = admin_presenter.get_user_count_message(users_count)
    await base_view.send_message(query.message, user_count_message)