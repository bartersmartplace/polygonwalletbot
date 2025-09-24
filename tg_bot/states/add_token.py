from aiogram.fsm.state import State, StatesGroup

class AddToken(StatesGroup):
    enter_address = State()
    enter_password = State()