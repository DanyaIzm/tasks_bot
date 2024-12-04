from aiogram.fsm.state import State, StatesGroup


class FindTaskStates(StatesGroup):
    find_task = State()


class FindTaskForm(StatesGroup):
    keyword = State()
