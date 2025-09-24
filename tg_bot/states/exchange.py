from aiogram.fsm.state import State, StatesGroup

class Exchange(StatesGroup):
    pool_info = State()
    confirm = State()
    enter_password = State()