from aiogram.fsm.state import State, StatesGroup

class PayNewAddress(StatesGroup):
    enter_password = State()