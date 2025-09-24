import re
from aiogram.types import CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from tg_bot.controllers import AdminController
from tg_bot.states import Broadcasting, Addbutton
from tg_bot.presenters.admin import AdminPresenter
from tg_bot.views.admin import AdminView
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.base import BaseView
from .admin_router import admin_router
from tg_bot.templates.buttons import text, callbacks


@admin_router.callback_query(callbacks.BroadcastingCallbackData.filter(F.option == text.MESSAGE_BROADCASTING_TEXT))
async def eng_message_entering(
    query: CallbackQuery,
    state: FSMContext,
    session,
    admin_presenter: AdminPresenter,
    admin_view: AdminView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    """
    Ask user to send english message
    """
    await query.answer()
    await state.clear()
    ask_message_entering = admin_presenter.ask_english_message_entering()
    await base_view.send_message(query, ask_message_entering)
    await state.set_state(Broadcasting.eng_message_enterning)


@admin_router.message(Broadcasting.eng_message_enterning)
async def rus_message_entering(
    message: Message,
    state: FSMContext,
    session,
    admin_presenter: AdminPresenter,
    admin_view: AdminView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    """
    1) Create empty rus and en list with buuton text
    2) Save russian message
    3) Ask user to send russian message
    """
    await state.clear()
    en_buttons_text = []
    en_buttons_link = []
    rus_buttons_text = []
    rus_buttons_link = []
    await state.update_data(en_buttons_text=en_buttons_text)
    await state.update_data(en_buttons_link=en_buttons_link)
    await state.update_data(rus_buttons_text=rus_buttons_text)
    await state.update_data(rus_buttons_link=rus_buttons_link)
    en_message = message.text
    await state.update_data(en_message=en_message)
    ask_message_entering = admin_presenter.ask_russian_message_entering()
    await base_view.send_message(message, ask_message_entering)
    await state.set_state(Broadcasting.rus_message_enterning)


@admin_router.message(Broadcasting.rus_message_enterning)
async def show_preview(
    message: Message,
    state: FSMContext,
    session,
    admin_presenter: AdminPresenter,
    admin_view: AdminView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    """
    1) Save russian message
    2) Show the user a russuian and english message to broadcast
    """
    rus_message = message.text
    await state.update_data(rus_message=rus_message)
    await __show_preview(message, admin_presenter, admin_view, state)


@admin_router.callback_query(callbacks.AddButtonCallbackData.filter(F.action == text.ADD_BUTTON_TEXT))
async def ask_to_add_en_buttons(
    query: CallbackQuery,
    state: FSMContext,
    session,
    admin_presenter: AdminPresenter,
    admin_view: AdminView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    """
    Ask user to enter english buttons
    """
    await query.answer()
    ask_en_text = admin_presenter.ask_english_buttons_entering()
    await base_view.send_message(query, ask_en_text)
    await state.set_state(Addbutton.eng_message_enterning)


@admin_router.message(Addbutton.eng_message_enterning)
async def show_preview_with_buttons(
    message: Message,
    state: FSMContext,
    session,
    admin_presenter: AdminPresenter,
    admin_view: AdminView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    """
    1) Save english buttons
    2) Ask user to enter russian buttons
    """
    data = await state.get_data()
    en_buttons_text = list(data.get("en_buttons_text"))
    en_buttons_link = list(data.get("en_buttons_link"))

    lines = message.text.split('\n')
    pattern = r"(.+?) - (https?://\S+)"
    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            print(f"Start math: {match}")
            button_text = match.group(1)
            button_link = match.group(2)
            en_buttons_text.append(button_text)
            en_buttons_link.append(button_link)

    await state.update_data(en_buttons_text=en_buttons_text, en_buttons_link=en_buttons_link)
    ask_rus_text = admin_presenter.ask_russian_buttons_entering()
    await base_view.send_message(message, ask_rus_text)
    await state.set_state(Addbutton.rus_message_enterning)


@admin_router.message(Addbutton.rus_message_enterning)
async def show_preview_with_buttons(
    message: Message,
    state: FSMContext,
    session,
    admin_presenter: AdminPresenter,
    admin_view: AdminView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    """
    1) Save russian buttons
    2) Show the user a russuian and english message to broadcast
    """
    data = await state.get_data()
    rus_buttons_text = list(data.get("rus_buttons_text", []))
    rus_buttons_link = list(data.get("rus_buttons_link", []))

    lines = message.text.split('\n')
    pattern = r"(.+?) - (https?://\S+)"

    for line in lines:
        match = re.match(pattern, line.strip())
        if match:
            button_text = match.group(1)
            button_link = match.group(2)
            rus_buttons_text.append(button_text)
            rus_buttons_link.append(button_link)

    await state.update_data(rus_buttons_text=rus_buttons_text, rus_buttons_link=rus_buttons_link)
    await __show_preview(message, admin_presenter, admin_view, state)


@admin_router.callback_query(callbacks.SendAdminMessageCallbackData.filter(F.action == text.SEND_ADMIN_MESSAGE_TEXT))
async def send_admin_message_to_users(
    query: CallbackQuery,
    state: FSMContext,
    session,
    admin_presenter: AdminPresenter,
    admin_view: AdminView,
    base_presenter: BasePresenter,
    base_view: BaseView
    ):
    """
    Start the message broadcast
    """
    await query.answer()
    admin_controller = AdminController(session)
    users = await admin_controller.get_all_users()
    data = await state.get_data()

    successful_message_count = 0
    for user in users:
        try:
            if user.language == "en":
                message = data["en_message"]
                buttons_text = data["en_buttons_text"]
                buttons_link = data["en_buttons_link"]
            else:
                message = data["rus_message"]
                buttons_text = data["rus_buttons_text"]
                buttons_link = data["rus_buttons_link"]

            await admin_view.send_preview_message(user.tg_id, message, buttons_text, buttons_link)
            successful_message_count += 1

        except Exception as e:
            print(str(e))

    finish_broadcasting_message = admin_presenter.get_broadcast_summary_message(successful_message_count)
    await base_view.send_message(query, finish_broadcasting_message)


async def __show_preview(
        message: Message,
        admin_presenter: AdminPresenter,
        admin_view: AdminView,
        state: FSMContext
        ):
    data = await state.get_data()
    await admin_view.send_preview_message(message.chat.id, data["en_message"], data["en_buttons_text"], data["en_buttons_link"])
    await admin_view.send_preview_message(message.chat.id, data["rus_message"], data["rus_buttons_text"], data["rus_buttons_link"])
    message_preview = admin_presenter.get_admin_message_preview()
    await admin_view.send_add_button_message(message.chat.id, message_preview)