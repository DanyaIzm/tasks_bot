from aiogram.fsm.state import State, StatesGroup


class RegistrationForm(StatesGroup):
    name = State()
    phone = State()
