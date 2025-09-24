from aiogram.fsm.state import State, StatesGroup

class AddressChanging(StatesGroup):
    address_address_entering = State()  # entering the address of the wallet