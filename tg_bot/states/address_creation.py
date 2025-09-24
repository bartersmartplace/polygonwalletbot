from aiogram.fsm.state import State, StatesGroup

class GenerateNewAddress(StatesGroup):
    password_entering = State()  # entering the password