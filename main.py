import asyncio
import logging
import sqlite3
import sys

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config
from middlewares.authentication_middleware import AuthenticationMiddleware
from middlewares.tasks_repository_injection_middleware import (
    TaskRepositoryInjectionMiddleware,
)
from middlewares.user_repository_injection_middleware import (
    UserRepositoryInjectionMiddleware,
)
from repositories.sqlite_repository import SqliteTaskRepository, SqliteUserRepository
from routers.add_task.add_task import router as add_task_router
from routers.filter_tasks.filter_tasks import router as filter_tasks_router
from routers.get_user_tasks.get_user_tasks import router as get_user_tasks_router
from routers.main import router as main_router
from routers.manage_tasks.manage_tasks import router as manage_tasks_router
from routers.registration.registration import router as registration_router


def create_tables(connection: sqlite3.Connection):
    connection.execute(
        "CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, name VARCHAR(255) NOT NULL, phone VARCHAR(12) NOT NULL)"
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            is_completed INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
        """
    )


async def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    config = load_config()

    # лучше использовать асинхронную библиотеку для работу с БД
    connection = sqlite3.connect("./database.db")

    create_tables(connection)

    dispatcher = Dispatcher()

    user_repository = SqliteUserRepository(connection)
    dispatcher.message.middleware(UserRepositoryInjectionMiddleware(user_repository))

    authenticated_router = Router()
    authenticated_router.message.middleware(AuthenticationMiddleware())

    task_repository = SqliteTaskRepository(connection)
    task_repository_injection_middleware = TaskRepositoryInjectionMiddleware(
        task_repository
    )
    add_task_router.message.middleware(task_repository_injection_middleware)
    get_user_tasks_router.message.middleware(task_repository_injection_middleware)
    manage_tasks_router.message.middleware(task_repository_injection_middleware)
    filter_tasks_router.message.middleware(task_repository_injection_middleware)

    authenticated_router.include_routers(
        add_task_router,
        get_user_tasks_router,
        manage_tasks_router,
        filter_tasks_router,
        main_router,
    )

    dispatcher.include_router(registration_router)
    dispatcher.include_router(authenticated_router)

    bot = Bot(
        token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
