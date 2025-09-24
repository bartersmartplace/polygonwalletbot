from aiogram.types import  Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from domain.common.errors import AppError
from .token_router import token_router
from tg_bot.controllers import StakeController
from tg_bot.presenters.token import TokenPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.token import TokenView
from tg_bot.views.base import BaseView


@token_router.message(Command("stake"))
async def stake_brtr_info(
    logging.info(f"/stake called by user {message.from_user.id}")
    await message.answer("Команда /stake получена, обрабатывается...")
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
    stake_controller = StakeController(session)
    
    try:
        stBRTR_balance, BRTR_balance, stakers_count, totalValueLocked = await stake_controller.get_stake_base_info(telegram_id)
        base_stake_info_message = token_presenter.get_stake_information(BRTR_balance, stBRTR_balance, stakers_count, totalValueLocked)
        await token_view.send_base_stake_info_message(telegram_id, base_stake_info_message)

        BRTR, BRTR_balance_in_wei = BRTR_balance.tokens[0]
        stBRTR, stBRTR_balance_in_wei = stBRTR_balance.tokens[0]
        await state.update_data(BRTR=BRTR)
        await state.update_data(stBRTR=stBRTR)
        await state.update_data(BRTR_balance=BRTR_balance_in_wei)
        await state.update_data(stBRTR_balance=stBRTR_balance_in_wei)

    except AppError as error:
        await state.clear()
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)