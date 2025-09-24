from aiogram import F
from aiogram.types import  Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from domain.common.errors import AppError
from domain.common.errors import InsufficientFundsError
from app.application.dto import UserDTO, TokenDTO
from app.config import (
    PAY_TOKEN_SYMBOL_TO_ADD_ERC20,
    PAY_TOKEN_DECIMALS,
    PRICE_TO_ADD_ERC20,
    PAY_TOKEN_SYMBOL_TO_ADD_ERC20_TO_EVERYONE,
    PAY_TOKEN_DECIMALS_TO_ADD_ERC20_TO_EVERYONE,
    PRICE_TO_ADD_ERC20_TO_EVERYONE
    )
from .token_router import token_router
from tg_bot.controllers import AddressController, TokenController, AdminController
from tg_bot.presenters.token import TokenPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.token import TokenView
from tg_bot.views.base import BaseView
from tg_bot.states import AddToken
from tg_bot.templates.buttons import callbacks, text


@token_router.callback_query(callbacks.PaymentForERC20CallbackData.filter(F.action == text.ADD_TOKEN))
async def start_add_ERC20(
    query: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
    session,
    token_presenter: TokenPresenter,
    token_view: TokenView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await query.answer()
    await state.clear()
    ask_contract_address = token_presenter.ask_to_enter_ERC20_contractr()
    await token_view.send_message_to_adding_ERC20(query.message, ask_contract_address)
    await state.set_state(AddToken.enter_address)


@token_router.message(AddToken.enter_address)
async def get_ERC20_information(
    message: Message,
    state: FSMContext,
    user: UserDTO,
    session,
    token_presenter: TokenPresenter,
    token_view: TokenView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    try:
        address = message.text.strip()
        token_controller = TokenController(session)
        token_data = await token_controller.get_ERC20_token(address)
        ask_to_add_erc20 = token_presenter.get_ask_to_add_erc20(token_data)
        await token_view.send_ask_to_add_ERC20(message, ask_to_add_erc20)
        await state.update_data(token=token_data)

    except AppError as error:
        await state.clear()
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)


@token_router.callback_query(callbacks.AddERC20.filter(F.action == text.ADD_TEXT))
async def choose_way_to_add_token(
    query: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
    session,
    token_presenter: TokenPresenter,
    token_view: TokenView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    await query.answer()
    data = await state.get_data()
    telegram_id = query.from_user.id
    token_controller = TokenController(session)
    user_tokens = await token_controller.get_user_tokens(telegram_id)
    choose_way_to_add_token_message = token_presenter.get_choose_way_to_add_token_message(
        data["token"],
        user_tokens,
        user.tokens_limit,
        PAY_TOKEN_SYMBOL_TO_ADD_ERC20,
        PAY_TOKEN_DECIMALS,
        PRICE_TO_ADD_ERC20,
        PAY_TOKEN_SYMBOL_TO_ADD_ERC20_TO_EVERYONE,
        PAY_TOKEN_DECIMALS_TO_ADD_ERC20_TO_EVERYONE,
        PRICE_TO_ADD_ERC20_TO_EVERYONE
    )
    await token_view.send_choose_way_to_add_token_message(query, choose_way_to_add_token_message)


@token_router.callback_query(callbacks.AddERC20.filter(F.action == text.ONLY_FOR_ME))
async def add_token_for_user(
    query: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
    session,
    token_presenter: TokenPresenter,
    token_view: TokenView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    try:
        await query.answer()
        telegram_id = query.from_user.id
        token_controller = TokenController(session)
        user_tokens = await token_controller.get_user_tokens(telegram_id)
        await state.update_data(way_to_add=text.ONLY_FOR_ME)
        if len(user_tokens) < user.tokens_limit:
            data = await state.get_data()
            await token_controller.add_user_token(telegram_id, data["token"])
            new_token_added_message = token_presenter.get_new_token_added_message()
            await base_view.send_message(query, new_token_added_message)
            await state.clear()

        else:
            address_controller = AddressController(session)
            token_balance = await address_controller.get_token_balance_for_tg_user(telegram_id, PAY_TOKEN_SYMBOL_TO_ADD_ERC20)
            _, balance = token_balance.tokens[0]
            # fix it later
            if balance < PRICE_TO_ADD_ERC20:
                raise InsufficientFundsError()
                
            enter_password_message = token_presenter.get_ask_password_entering_message()
            await base_view.send_message(query, enter_password_message)
            await state.set_state(AddToken.enter_password)
        
    except AppError as error:
        await state.clear()
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(query.message, error_message)


@token_router.callback_query(callbacks.AddERC20.filter(F.action == text.PAY_FOR_LISTING))
async def add_token_for_everyone(
    query: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
    session,
    token_presenter: TokenPresenter,
    token_view: TokenView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    try:
        await query.answer()
        telegram_id = query.from_user.id
        address_controller = AddressController(session)
        token_balance = await address_controller.get_token_balance_for_tg_user(telegram_id, PAY_TOKEN_SYMBOL_TO_ADD_ERC20)
        _, balance = token_balance.tokens[0]

        # fix it later
        if balance < PRICE_TO_ADD_ERC20_TO_EVERYONE:
            raise InsufficientFundsError()
        await state.update_data(way_to_add=text.PAY_FOR_LISTING)
        enter_password_message = token_presenter.get_ask_password_entering_message()
        await base_view.send_message(query, enter_password_message)
        await state.set_state(AddToken.enter_password)
        
    except AppError as error:
        await state.clear()
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(query.message, error_message)
    

@token_router.message(AddToken.enter_password)
async def ask_password(
    message: Message,
    state: FSMContext,
    user: UserDTO,
    session,
    token_presenter: TokenPresenter,
    token_view: TokenView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    telegram_id = message.from_user.id
    password = message.text.strip()
    try:
        data = await state.get_data()
        token_controller = TokenController(session)

        wait_message = base_presenter.get_wait_message()
        sent_wait_message = await base_view.send_message(message, wait_message)
        way_to_add = data["way_to_add"]
        if way_to_add == text.ONLY_FOR_ME:
            tx_hash = await token_controller.buy_slot_for_new_user_token(
                telegram_id,
                password,
                PAY_TOKEN_SYMBOL_TO_ADD_ERC20,
                PRICE_TO_ADD_ERC20,
                data["token"],
            )
            paid_message = token_presenter.get_paid_message(
                tx_hash,
                PAY_TOKEN_SYMBOL_TO_ADD_ERC20,
                PAY_TOKEN_DECIMALS,
                PRICE_TO_ADD_ERC20,
                )
            await token_view.send_paid_message(sent_wait_message, paid_message)
            await token_controller.add_user_token(telegram_id, data["token"])
            new_token_added_message = token_presenter.get_new_token_added_message()
            await base_view.send_message(message, new_token_added_message)
        
        else:
            tx_hash = await token_controller.buy_slot_for_new_base_token(
                telegram_id,
                password,
                PAY_TOKEN_SYMBOL_TO_ADD_ERC20_TO_EVERYONE,
                PRICE_TO_ADD_ERC20_TO_EVERYONE,
                data["token"],
                )
            paid_message = token_presenter.get_paid_message(
                tx_hash,
                PAY_TOKEN_SYMBOL_TO_ADD_ERC20_TO_EVERYONE,
                PAY_TOKEN_DECIMALS_TO_ADD_ERC20_TO_EVERYONE,
                PRICE_TO_ADD_ERC20_TO_EVERYONE,
                )
            await token_view.send_paid_message(sent_wait_message, paid_message)
            await token_controller.add_base_token(data["token"])

            admin_controller = AdminController(session)
            users = await admin_controller.get_all_users()
            for user in users:
                try:
                    if user.language == "en":
                        message_to_send = f"Added a new token to the wallet - {data["token"].symbol}."
                    else:
                        message_to_send = f"Добавлен новый токен в кошелек - {data["token"].symbol}."

                    await base_view.send_message_by_id(user.tg_id, message_to_send)

                except Exception as e:
                    print(str(e))
            await state.clear()
        
    except AppError as error:
        await state.clear()
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, error_message)