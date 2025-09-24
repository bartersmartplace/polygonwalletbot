from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from tg_bot.controllers import AdminController
from tg_bot.presenters.admin import AdminPresenter
from tg_bot.views.admin import AdminView
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.base import BaseView
from .admin_router import admin_router
from tg_bot.templates.buttons import text, callbacks


@admin_router.message(Command("admin"))
async def admin_panel(
    message: Message,
    state: FSMContext,
    session,
    admin_presenter: AdminPresenter,
    admin_view: AdminView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await state.clear()
    admin_panel_message = admin_presenter.get_admin_menu_message()
    await admin_view.send_admin_menu_message(message.chat.id, admin_panel_message)
    