from aiogram.types import  Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from tg_bot.presenters.swap import SwapPresenter
from tg_bot.views.swap import SwapView
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.base import BaseView
from .swap_router import swap_router


@swap_router.message(Command("swap"))
async def swap(
    message: Message,
    state: FSMContext,
    session,
    swap_presenter: SwapPresenter,
    swap_view: SwapView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await state.clear()
    brub_manual = swap_presenter.get_swap_manual()
    await base_view.send_message(message, brub_manual)


