from aiogram.fsm.state import State, StatesGroup

class Unstake(StatesGroup):
    enter_amount = State()
    enter_password = State()