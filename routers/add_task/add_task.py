from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.main_keyboard import get_main_keyboard
from repositories.repository import TaskRepository

from .states import AddTaskForm

router = Router()


@router.message(F.text == "Добавить задачу")
@router.message(Command("add"))
async def add_task_handler(message: Message, state: FSMContext):
    await message.answer("Напиши название задачи", reply_markup=ReplyKeyboardRemove())

    await state.set_state(AddTaskForm.name)


@router.message(AddTaskForm.name)
async def add_task_name_step_handler(message: Message, state: FSMContext):
    name = message.text

    await state.set_data({"name": name})

    await message.answer("Напиши описание задачи")

    await state.set_state(AddTaskForm.description)


@router.message(AddTaskForm.description)
async def add_task_description_step_handler(
    message: Message, state: FSMContext, task_repository: TaskRepository
):
    description = message.text

    await state.update_data({"description": description})

    task_data = await state.get_data()
    user_id = message.from_user.id

    task_repository.add_task(
        user_id=user_id, name=task_data["name"], description=task_data["description"]
    )

    await message.answer(
        "Задача была успешно добавлена", reply_markup=get_main_keyboard()
    )

    await state.clear()
