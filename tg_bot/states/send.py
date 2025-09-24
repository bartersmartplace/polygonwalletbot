from aiogram.fsm.state import State, StatesGroup

class Send(StatesGroup):
    enter_recipient = State()
    enter_amount = State()
    enter_password = State()
    confirm = State()