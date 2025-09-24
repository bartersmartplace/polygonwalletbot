from aiogram.types import  Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from tg_bot.states import AddressChanging
from .user_router import user_router
from tg_bot.controllers import UserController
from tg_bot.presenters.user import UserPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.user import UserView


@user_router.message(Command("addresses"))
async def get_addresses(
    message: Message,
    state: FSMContext,
    session,
    user_presenter: UserPresenter,
    user_view: UserView,
    base_presenter: BasePresenter,
    ):
    await state.clear()
    telegram_id = message.from_user.id
    user_controller = UserController(session)
    addresses_list = await user_controller.get_address_list(telegram_id)
    address_list_message = user_presenter.get_addresses_list_message(addresses_list)
    await user_view.send_address_list_message(message, address_list_message)
    if addresses_list:
        await state.set_state(AddressChanging.address_address_entering)
        await state.update_data(addresses_list=addresses_list)