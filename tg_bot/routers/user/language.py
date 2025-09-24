from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from .user_router import user_router
from tg_bot.controllers import UserController
from tg_bot.presenters.user import UserPresenter
from tg_bot.presenters.base import BasePresenter
from tg_bot.views.user import UserView
from tg_bot.views.base import BaseView
from tg_bot.templates.buttons import text, callbacks


@user_router.callback_query(callbacks.LanguageCallbackData.filter())
async def change_language(
    query: CallbackQuery,
    state: FSMContext,
    session,
    user_presenter: UserPresenter,
    user_view: UserView,
    base_presenter: BasePresenter,
    base_view: BaseView,
    callback_data: callbacks.LanguageCallbackData
):
    language_map = {
        text.ENG_TEXT: ("en", text.ENG_TEXT),
        text.RUS_TEXT: ("rus", text.RUS_TEXT),
    }

    telegram_id = query.from_user.id
    await state.clear()
    user_controller = UserController(session)    
    language, message_text = language_map.get(callback_data.language, ("en", text.ENG_TEXT))
    await user_controller.update_language(telegram_id=telegram_id, language=language)
    language_changed_message = user_presenter.get_language_changed_message(message_text.lower())
    await base_view.send_message(query.message, language_changed_message)