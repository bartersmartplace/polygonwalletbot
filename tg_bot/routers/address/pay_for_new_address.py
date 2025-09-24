from aiogram.types import  CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from domain.common.errors import AppError
from app.config import (
    PAY_TOKEN_SYMBOL_TO_GENERATE_NEW_ADDRESS,
    PRICE_TO_GENERATE_NEW_ADDRESS,
    PAY_TOKEN_DECIMALS
    )
from .address_router import address_router
from tg_bot.states import PayNewAddress
from tg_bot.controllers import AddressController, ValidatorController
from tg_bot.presenters.address import AddressPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.address import AddressView
from tg_bot.views.base import BaseView
from tg_bot.templates.buttons import text, callbacks


@address_router.callback_query(callbacks.PaymentForNewAddressCallbackData.filter(F.action == text.PAY_TEXT))
async def enter_password(
    query: CallbackQuery,
    state: FSMContext,
    address_presenter: AddressPresenter,
    address_view: AddressView,
    base_view: BaseView
    ):
    await query.answer()
    data = await state.get_data()
    if "password" in data:
        enter_password_message = address_presenter.get_password_entering_for_new_address_message()
        await base_view.send_message(query, enter_password_message)
        await state.set_state(PayNewAddress.enter_password)


@address_router.message(PayNewAddress.enter_password)
async def payment(
        message: Message,
        state: FSMContext,
        session,
        address_presenter: AddressPresenter,
        address_view: AddressView,
        base_presenter: BasePresenter,
        base_view: BaseView
        ):
    try:
        telegram_id = message.from_user.id
        telegram_name = message.from_user.first_name
        username = message.from_user.username
        password = message.text.strip()
        data = await state.get_data()
        validator_controller = ValidatorController(session)
        await validator_controller.validate_password(telegram_id, password)
        address_controller = AddressController(session)

        wait_message = base_presenter.get_wait_message()
        sent_wait_message = await base_view.send_message(message, wait_message)

        tx_hash = await address_controller.buy_new_address(telegram_id, password)
        successful_paying_message = address_presenter.get_tx_message(
            PRICE_TO_GENERATE_NEW_ADDRESS / 10 ** PAY_TOKEN_DECIMALS,
            PAY_TOKEN_SYMBOL_TO_GENERATE_NEW_ADDRESS,
            "0xBe10a6B5d6C4c63F4FCEE30c73ba7C029f3dC4C1",
            tx_hash
        )
        await address_view.send_message_of_successful_paying(sent_wait_message, successful_paying_message)
        address = await address_controller.create_account(telegram_id, data["password"], telegram_name, username)
        address_generation_message = address_presenter.get_successful_address_generation_message(address)
        await address_view.send_address_generation_message(telegram_id, address_generation_message)
        await state.clear()

    except AppError as error:
        await state.clear()
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)