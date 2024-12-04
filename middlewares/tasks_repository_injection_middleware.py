from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from repositories.repository import TaskRepository


class TaskRepositoryInjectionMiddleware(BaseMiddleware):
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        data["task_repository"] = self._repository

        return await handler(event, data)
