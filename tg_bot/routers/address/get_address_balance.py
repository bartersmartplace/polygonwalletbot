from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F
from domain.common.errors import AppError
from .address_router import address_router
from tg_bot.controllers import AddressController
from tg_bot.presenters.address import AddressPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.address import AddressView
from tg_bot.views.base import BaseView
from tg_bot.templates.buttons import text, callbacks
from app.application.service.common.error import AddressNotFoundError

@address_router.message(Command("assets"))
async def get_balance(
    message: Message,
    state: FSMContext,
    session,
    address_presenter: AddressPresenter,
    address_view: AddressView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    try:
        await state.clear()
        telegram_id = message.from_user.id
        address_controller = AddressController(session)

        balances = await address_controller.get_account_balance(telegram_id)
        balance_message = address_presenter.get_balances_message(balances)
        await address_view.send_balance_message(message, balance_message)

    except AppError as error:
        await state.clear()
        if isinstance(error, AddressNotFoundError):
            set_active_address_message = address_presenter.get_active_address_is_not_set_message()
            await base_view.send_message(message, set_active_address_message)
            return
        
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)


@address_router.callback_query(callbacks.BalanceCallbackData.filter(F.action == text.BACK_SYMBOL))
async def handle_balance_callback(
    query: CallbackQuery,
    state: FSMContext,
    session,
    address_presenter: AddressPresenter,
    address_view: AddressView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await query.answer()
    try:
        await state.clear()
        telegram_id = query.from_user.id
        address_controller = AddressController(session)

        balances = await address_controller.get_account_balance(telegram_id)
        balance_message = address_presenter.get_balances_message(balances)
        await address_view.send_balance_message(query.message, balance_message)

    except AppError as error:
        await state.clear()
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(query, error_message)