from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from formatters.task_list_formatter import get_formatted_task_list
from repositories.repository import TaskRepository

router = Router()


@router.message(F.text == "Список задач")
@router.message(Command("list"))
async def get_user_tasks_handler(message: Message, task_repository: TaskRepository):
    user_id = message.from_user.id

    tasks = task_repository.get_tasks_by_user_id(user_id)

    if tasks:
        await message.answer(**get_formatted_task_list(tasks))
    else:
        await message.answer("Вы пока не добавили ни одной задачи")
