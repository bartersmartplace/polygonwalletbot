from aiogram.types import  Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from tg_bot.presenters.swap import SwapPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.swap import SwapView
from tg_bot.views.base import BaseView
from .swap_router import swap_router
from tg_bot.templates.buttons import text, callbacks


@swap_router.message(Command("brub"))
async def brub_manual(
    message: Message,
    state: FSMContext,
    session,
    swap_presenter: SwapPresenter,
    swap_view: SwapView,
    base_presenter: BasePresenter,
    ):
    telegram_id = message.from_user.id
    await state.clear()
    brub_manual = swap_presenter.get_brub_manual()
    await swap_view.send_brub_manual(telegram_id, brub_manual)


@swap_router.callback_query(callbacks.BrubCallbackData.filter(F.action == text.RETURN_BRUB_TEXT))
async def return_brub(
    query: CallbackQuery,
    state: FSMContext,
    session,
    swap_presenter: SwapPresenter,
    swap_view: SwapView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await query.answer()
    await state.clear()
    return_brub_message = swap_presenter.get_return_brub_message()
    await base_view.send_message(query, return_brub_message)