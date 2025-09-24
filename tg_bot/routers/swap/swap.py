from aiogram.types import  Message, CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from domain.common.errors import AppError
from tg_bot.states import Exchange
from tg_bot.controllers import TokenController
from tg_bot.presenters.swap import SwapPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.swap import SwapView
from tg_bot.views.base import BaseView
from .swap_router import swap_router
from tg_bot.templates.buttons import text, callbacks


@swap_router.message(F.text.casefold().startswith("swap "))
async def swap_info(
    message: Message,
    state: FSMContext,
    session,
    swap_presenter: SwapPresenter,
    swap_view: SwapView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await state.clear()
    _, amount_to_sell, token_in, token_out = message.text.split(" ")
    
    try:
        token_controller = TokenController(session)
        trade = await token_controller.get_trade_parameters(token_in, token_out, amount_to_sell)
        trade_message = swap_presenter.get_swap_parameters_message(trade)
        await swap_view.send_swap_parameters_message(message, trade_message)
        await state.update_data(trade=trade)
        await state.set_state(Exchange.confirm)

    except AppError as error:
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)
    

@swap_router.callback_query(callbacks.SwapCallbackData.filter(F.action == text.CANCEL_TEXT), Exchange.confirm)
async def cancel_trade_operations(
    query: CallbackQuery,
    state: FSMContext,
    session,
    swap_presenter: SwapPresenter,
    swap_view: SwapView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await state.clear()
    await query.answer()
    trade_message = swap_presenter.get_cancel_trade_operation_message()
    await base_view.send_message(query.message, trade_message)


@swap_router.callback_query(callbacks.SwapCallbackData.filter(F.action == text.CONFIRM_TEXT), Exchange.confirm)
async def ask_password(
    query: CallbackQuery,
    state: FSMContext,
    session,
    swap_presenter: SwapPresenter,
    swap_view: SwapView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await query.answer()
    trade_message = swap_presenter.get_ask_password_message()
    await base_view.send_message(query.message, trade_message)
    await state.set_state(Exchange.enter_password)


@swap_router.message(Exchange.enter_password)
async def make_trade(
    message: Message,
    state: FSMContext,
    session,
    swap_presenter: SwapPresenter,
    swap_view: SwapView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    telegram_id = message.from_user.id
    password = message.text.strip()
    data = await state.get_data()
    try:
        trade = data["trade"]
        token_controller = TokenController(session)

        wait_message = base_presenter.get_wait_message()
        sent_wait_message = await base_view.send_message(message, wait_message)
        
        tx_hash = await token_controller.make_trade_parameters(telegram_id, password, trade)

    except AppError as error:
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)
    
    finally:
        await state.clear()