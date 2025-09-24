from aiogram.types import  Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from domain.common.errors import AppError, InsufficientFundsError
from app.application.dto import TokenDTO
from .token_router import token_router
from tg_bot.controllers import StakeController, ValidatorController
from tg_bot.presenters.token import TokenPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.token import TokenView
from tg_bot.views.base import BaseView
from tg_bot.states import Unstake
from tg_bot.templates.buttons import text, callbacks


@token_router.message(F.text.casefold().startswith("burn "))
async def stop_staking_brtr(
    message: Message,
    state: FSMContext,
    user,
    session,
    token_presenter: TokenPresenter,
    token_view: TokenView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await state.clear()
    telegram_id = message.from_user.id
    _, amount, password = message.text.split(" ")
    try:
        wait_message = base_presenter.get_wait_message()
        sent_wait_message = await base_view.send_message(message, wait_message)

        stake_controller = StakeController(session)
        tx_hash = await stake_controller.stop_stake_brtr_use_case(telegram_id, password, amount)
        stake_tx_message = token_presenter.get_stop_brtr_stake_message(tx_hash, float(amount))
        await token_view.send_stake_tx_message(sent_wait_message, stake_tx_message)

    except AppError as error:
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)


@token_router.callback_query(callbacks.StakeCallbackData.filter(F.action == text.REMOVE_TEXT))
async def ask_amount_entering(
    query: CallbackQuery,
    state: FSMContext,
    session,
    token_presenter: TokenPresenter,
    token_view: TokenView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    try:
        await query.answer()
        await state.set_state(Unstake.enter_amount)
        ask_amount_message = token_presenter.ask_how_much_brtr_to_remove_from_stake()
        await base_view.send_message(query, ask_amount_message)

    except AppError as error:
        await base_view.send_error_message(query, str(error))


@token_router.message(Unstake.enter_amount)
async def ask_password_entering(
    message: Message,
    state: FSMContext,
    session,
    token_presenter: TokenPresenter,
    token_view: TokenView,
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
        if ("stBRTR" in data) and ("stBRTR_balance" in data):
            BRTR: TokenDTO = data['stBRTR']
            balance = int(data['stBRTR_balance'])

            if int(amount*10**BRTR.decimal) > balance:
                raise InsufficientFundsError("Insufficient balance to complete the transaction.")
        
        await state.update_data(amount=amount)
        submit_stake_message = token_presenter.get_ask_password_entering_message()
        await base_view.send_message(message, submit_stake_message)
        await state.set_state(Unstake.enter_password)
    except AppError as error:
        await state.clear()
        await base_view.send_error_message(message, str(error))


@token_router.message(Unstake.enter_password)
async def finish_stake(
    message: Message,
    state: FSMContext,
    session,
    token_presenter: TokenPresenter,
    token_view: TokenView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    telegram_id = message.from_user.id
    password = message.text.strip()
    data =await state.get_data()
    amount = float(data["amount"])
    stake_controller = StakeController(session)
    
    try:
        wait_message = base_presenter.get_wait_message()
        sent_wait_message = await base_view.send_message(message, wait_message)

        tx_hash = await stake_controller.stop_stake_brtr_use_case(telegram_id, password, amount)
        stake_tx_message = token_presenter.get_stop_brtr_stake_message(tx_hash, float(amount))
        await token_view.send_stake_tx_message(sent_wait_message, stake_tx_message)
        await state.clear()

    except AppError as error:
        await state.clear()
        await base_view.send_error_message(message, str(error))