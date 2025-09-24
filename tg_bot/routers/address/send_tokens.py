from aiogram.types import  CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from domain.common.errors import AppError, InsufficientFundsError
from .address_router import address_router
from tg_bot.states import Send
from tg_bot.controllers import AddressController, TokenController, ValidatorController
from tg_bot.presenters.address import AddressPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.address import AddressView
from tg_bot.views.base import BaseView
from tg_bot.templates.buttons import callbacks, text


@address_router.message(F.text.casefold().startswith("send "))
async def send_tokens(
        message: Message,
        state: FSMContext,
        session,
        address_presenter: AddressPresenter,
        address_view: AddressView,
        base_presenter: BasePresenter,
        base_view: BaseView
        ):
    _, amount, token_symbol, recipient, password = message.text.split(" ")
    try:
        await state.clear()
        telegram_id = message.from_user.id
        token_symbol = token_symbol.upper()
        address_controller = AddressController(session)

        wait_message = base_presenter.get_wait_message()
        sent_wait_message = await base_view.send_message(message, wait_message)

        if recipient.startswith("@"):
           recipient = str(recipient[1:])
           tx_hash = await address_controller.send_tokens(telegram_id, password, token_symbol, amount, tg_recipient=recipient)

        else:
           tx_hash = await address_controller.send_tokens(telegram_id, password, token_symbol, amount, external_recipient=recipient)
        
        send_message = address_presenter.get_tx_message(float(amount), token_symbol, recipient, tx_hash)
        await address_view.sent_transaction_message(sent_wait_message, send_message)

    except AppError as error:
        await base_view.send_error_message(message, str(error))


@address_router.callback_query(callbacks.SendCallbackData.filter(F.token == ""))
async def choose_token(
    query: CallbackQuery,
    state: FSMContext,
    session,
    address_presenter: AddressPresenter,
    address_view: AddressView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    telegram_id = query.from_user.id
    try:
        await state.clear()
        await query.answer()
        token_controller = TokenController(session)
        tokens = await token_controller.get_sendable_tokens(telegram_id)
        send_token_message = address_presenter.get_choose_token_message()
        await address_view.send_tokens_to_send_message(query, send_token_message, tokens)

    except AppError as error:
        await base_view.send_error_message(query, str(error))


@address_router.callback_query(callbacks.SendCallbackData.filter())
async def ask_recipient_address(
    query: CallbackQuery,
    callback_data: callbacks.SendCallbackData,
    session,
    state: FSMContext,
    address_presenter: AddressPresenter,
    address_view: AddressView,
    base_presenter: BasePresenter,
    ):
    await state.clear()
    await query.answer()
    ask_enter_recipient_address = address_presenter.get_enter_recipient_message()
    await address_view.send_ask_recipient_message(query, ask_enter_recipient_address)
    await state.update_data(token=callback_data.token.upper())
    await state.set_state(Send.enter_recipient)


@address_router.message(Send.enter_recipient)
async def ask_send_amount(
        message: Message,
        state: FSMContext,
        session,
        address_presenter: AddressPresenter,
        address_view: AddressView,
        base_presenter: BasePresenter,
        base_view: BaseView
        ):
    telegram_id = message.from_user.id    
    try:
        recipient = message.text.strip()
        data = await state.get_data()
        validator_controller = ValidatorController(session)
        await state.update_data(recipient=recipient) 
        if recipient.startswith("@"):
            recipient = str(recipient[1:])
            address = await validator_controller.validate_recipient(tg_recipient=recipient)
        else:
            address = await validator_controller.validate_recipient(external_recipient=recipient)
        
        await state.update_data(address=address)
        address_controller = AddressController(session)
        token_balance = await address_controller.get_token_balance_for_tg_user(telegram_id, data["token"])
        enter_amount_message = address_presenter.get_enter_amount_message(token_balance)
        await base_view.send_message(message, enter_amount_message)
        token, balance = token_balance.tokens[0]
        await state.update_data(balance=(balance / 10**token.decimal))
        await state.set_state(Send.enter_amount)

    except AppError as error:
        await state.clear()
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)


@address_router.message(Send.enter_amount)
async def ask_confirmation(
        message: Message,
        state: FSMContext,
        session,
        address_presenter: AddressPresenter,
        address_view: AddressView,
        base_presenter: BasePresenter,
        base_view: BaseView
        ):
    amount = message.text.strip()
    try:
        data = await state.get_data()
        validator_controller = ValidatorController(session)
        validator_controller.validate_amount(amount)
        amount = float(amount)
        await state.update_data(amount=amount)
        if amount > float(data['balance']):
            InsufficientFundsError("Insufficient balance to complete the transaction.")
        submit_tx_message = address_presenter.get_submit_tx_message(amount, data["token"], data["address"])
        await address_view.send_ask_tx_confirmation(message, submit_tx_message)
        await state.set_state(Send.confirm)

    except AppError as error:
        await state.clear()
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)
    

@address_router.callback_query(callbacks.ConfirmCallbackData.filter(F.action == text.CONFIRM_TEXT), Send.confirm)
async def ask_password_entering(
        query: CallbackQuery,
        state: FSMContext,
        session,
        address_presenter: AddressPresenter,
        address_view: AddressView,
        base_presenter: BasePresenter,
        base_view: BaseView,
        ):
    await query.answer()
    submit_tx_message = address_presenter.get_ask_password_entering_message()
    await base_view.send_message(query, submit_tx_message)
    await state.set_state(Send.enter_password)


@address_router.message(Send.enter_password)
async def send_tx(
        message: Message,
        state: FSMContext,
        session,
        address_presenter: AddressPresenter,
        address_view: AddressView,
        base_presenter: BasePresenter,
        base_view: BaseView
        ):
    data = await state.get_data()
    telegram_id = message.from_user.id
    token_symbol = data["token"]
    password = message.text.strip()
    amount = data["amount"]
    address = data["address"]
    recipient = data["recipient"]
    address_controller = AddressController(session)

    wait_message = base_presenter.get_wait_message()
    sent_wait_message = await base_view.send_message(message, wait_message)
    
    try:
        tx_hash = await address_controller.send_tokens(telegram_id, password, token_symbol, amount, external_recipient=address)
        send_message = address_presenter.get_tx_message(amount, token_symbol, recipient, tx_hash)
        await address_view.sent_transaction_message(sent_wait_message, send_message)
    except AppError as error:
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)
    
    finally:
        await state.clear()