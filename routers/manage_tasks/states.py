from aiogram.fsm.state import State, StatesGroup


class CompleteTaskForm(StatesGroup):
    id = State()
