from aiogram.fsm.state import State, StatesGroup

class Broadcasting(StatesGroup):
    eng_message_enterning = State()
    rus_message_enterning = State()