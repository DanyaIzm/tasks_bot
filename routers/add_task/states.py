from aiogram.fsm.state import State, StatesGroup


class AddTaskForm(StatesGroup):
    name = State()
    description = State()
