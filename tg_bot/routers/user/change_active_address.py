from aiogram.types import  Message
from aiogram.fsm.context import FSMContext
from domain.common.errors import AppError
from app.application.dto import AddressDTO
from tg_bot.controllers import AddressController
from tg_bot.states import AddressChanging
from .user_router import user_router
from tg_bot.controllers import UserController, AddressController
from tg_bot.presenters.user import UserPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.user import UserView
from tg_bot.views.base import BaseView
from tg_bot.presenters.address import AddressPresenter
from tg_bot.views.address import AddressView



@user_router.message(AddressChanging.address_address_entering)
async def change_address(
    message: Message,
    state: FSMContext,
    session,
    user_presenter: UserPresenter,
    user_view: UserView,
    base_presenter: BasePresenter,
    base_view: BaseView,
    address_presenter: AddressPresenter,
    address_view: AddressView,
    ):
    telegram_id = message.from_user.id
    address = message.text.strip()
    try:
        # update active address
        data = await state.get_data()
        addresses_list: AddressDTO = data["addresses_list"]
        user_controller = UserController(session)
        await user_controller.update_active_address(telegram_id, address, addresses_list)
        update_address_message = user_presenter.get_active_address_update_message()
        await user_view.send_address_update_message(message, update_address_message)

        # send balance
        address_controller = AddressController(session)
        balances = await address_controller.get_account_balance(telegram_id)
        balance_message = address_presenter.get_balances_message(balances)
        await address_view.send_balance_message(message, balance_message)
        

    except AppError as error:
        error_message = base_presenter.get_error_message(error)
        await base_view.send_error_message(message, str(error))
    
    finally:
        await state.clear()