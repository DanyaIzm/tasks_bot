from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.main_keyboard import get_main_keyboard
from repositories.repository import TaskRepository

from .states import CompleteTaskForm

router = Router()


@router.message(F.text == "Отметить выполненной")
@router.message(Command("complete"))
async def complete_task_handler(message: Message, state: FSMContext):
    await message.answer(
        "Напишите id задачи, которую хотите завершить",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(CompleteTaskForm.id)


@router.message(CompleteTaskForm.id)
async def complete_task_id_step_handler(
    message: Message, state: FSMContext, task_repository: TaskRepository
):
    task_id = int(message.text)

    task = task_repository.get(task_id)

    if task is None:
        await message.answer(
            "Такой задачи не существует", reply_markup=get_main_keyboard()
        )
        await state.clear()
        return

    task.is_completed = True

    task_repository.update(task)

    await message.answer(
        "Задача была успешно завершена", reply_markup=get_main_keyboard()
    )

    await state.clear()


@router.message(F.text == "Удалить завершённые")
@router.message(F.text == "Удалить завершенные")
@router.message(Command("flush"))
async def flush_tasks_handler(message: Message, task_repository: TaskRepository):
    task_repository.delete_completed()

    await message.answer("Удалены все завершённые задачи")
