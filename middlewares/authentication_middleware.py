from collections.abc import Awaitable
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from repositories.repository import UserRepository


class AuthenticationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_repository: UserRepository = data["user_repository"]

        user = user_repository.find(event.from_user.id)

        if user is None:
            await event.answer(
                "Кажется, вы не зарегистрировались.\nНапишите команду /start, чтобы пройти процедуру регистрации"
            )
        else:
            return await handler(event, data)
