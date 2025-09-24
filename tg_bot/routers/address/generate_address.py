from aiogram.fsm.context import FSMContext
from aiogram.types import  Message
from aiogram import F
from aiogram.types import CallbackQuery
from domain.common.errors import AppError
from app.application.service.common.error import MaxAddressesExistError
from app.config import (
    PAY_TOKEN_SYMBOL_TO_GENERATE_NEW_ADDRESS,
    PRICE_TO_GENERATE_NEW_ADDRESS,
    PAY_TOKEN_DECIMALS
    )
from .address_router import address_router
from tg_bot.states import GenerateNewAddress
from tg_bot.controllers import AddressController
from tg_bot.presenters.address import AddressPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.address import AddressView
from tg_bot.views.base import BaseView
from tg_bot.templates.buttons import text, callbacks


@address_router.callback_query(callbacks.NewAddressCallbackData.filter(F.action == text.ADD_NEW_ADDRESS_TEXT))
async def generate_address_information(
    query: CallbackQuery,
    state: FSMContext,
    address_presenter: AddressPresenter,
    address_view: AddressView,
    base_presenter: BasePresenter,
    base_view: BaseView,
    ):
    await state.clear()
    await query.answer()
    await state.set_state(GenerateNewAddress.password_entering)
    generate_address_information_message = address_presenter.get_generate_address_information_message()
    await base_view.send_message(query, generate_address_information_message)


@address_router.message(GenerateNewAddress.password_entering)
async def enter_password(
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
        address_controller = AddressController(session)
        telegram_id = message.from_user.id
        password = message.text.strip()
        tg_name = message.from_user.first_name
        username = message.from_user.username
        address = await address_controller.create_account(telegram_id, password, tg_name, username)
        address_generation_message = address_presenter.get_successful_address_generation_message(address)
        await address_view.send_address_generation_message(telegram_id, address_generation_message)
        
    except AppError as error:
        await state.clear()
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)
        if isinstance(error, MaxAddressesExistError):
            generate_new_address_message = address_presenter.get_generate_new_address_message(
                PAY_TOKEN_SYMBOL_TO_GENERATE_NEW_ADDRESS,
                PAY_TOKEN_DECIMALS,
                PRICE_TO_GENERATE_NEW_ADDRESS
                )
            await address_view.send_message_to_start_generating_new_address(telegram_id, generate_new_address_message)
            await state.update_data(password=password)