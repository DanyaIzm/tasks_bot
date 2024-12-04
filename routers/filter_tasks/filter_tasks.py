from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from formatters.task_list_formatter import get_formatted_task_list
from keyboards.main_keyboard import get_main_keyboard
from repositories.repository import TaskRepository

from .states import FindTaskForm, FindTaskStates

router = Router()


@router.message(F.text == "Найти задачу")
@router.message(Command("find"))
async def find_task_handler(message: Message, state: FSMContext):
    buttons = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="По ключевому слову"),
            ],
            [
                KeyboardButton(text="Завершённые"),
                KeyboardButton(text="Незавершённые"),
            ],
        ],
        resize_keyboard=True,
    )

    await message.answer("Выберите критерий поиска", reply_markup=buttons)

    await state.set_state(FindTaskStates.find_task)


@router.message(FindTaskStates.find_task, F.text == "Завершённые")
async def find_completed_tasks_handler(
    message: Message, state: FSMContext, task_repository: TaskRepository
):
    tasks = task_repository.find_completed()

    if not tasks:
        await message.answer("Ничего не найдено", reply_markup=get_main_keyboard())
    else:
        await message.answer(
            "Нашлись следующие завершённые задачи", reply_markup=get_main_keyboard()
        )
        await message.answer(**get_formatted_task_list(tasks))

    await state.clear()


@router.message(FindTaskStates.find_task, F.text == "Незавершённые")
async def find_uncompleted_tasks_handler(
    message: Message, state: FSMContext, task_repository: TaskRepository
):
    tasks = task_repository.find_uncompleted()

    if not tasks:
        await message.answer("Ничего не найдено", reply_markup=get_main_keyboard())
    else:
        await message.answer(
            "Нашлись следующие незавершённые задачи", reply_markup=get_main_keyboard()
        )
        await message.answer(**get_formatted_task_list(tasks))

    await state.clear()


@router.message(FindTaskStates.find_task, F.text == "По ключевому слову")
async def find_task_by_keyword_handler(message: Message, state: FSMContext):
    await message.answer(
        "Введите ключевые слова для поиска", reply_markup=ReplyKeyboardRemove()
    )

    await state.set_state(FindTaskForm.keyword)


@router.message(FindTaskForm.keyword)
async def find_task(
    message: Message, state: FSMContext, task_repository: TaskRepository
):
    keyword = message.text

    tasks = task_repository.get_by_keyword(keyword)

    if not tasks:
        await message.answer("Ничего не найдено", reply_markup=get_main_keyboard())
    else:
        await message.answer(
            "Нашлись следующие задачи", reply_markup=get_main_keyboard()
        )
        await message.answer(**get_formatted_task_list(tasks))

    await state.clear()
