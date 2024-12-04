from aiogram import Router
from aiogram.types import Message

from keyboards.main_keyboard import get_main_keyboard

router = Router()


@router.message()
async def unknown_command_handler(message: Message) -> None:
    await message.answer("Неизвестная команда", reply_markup=get_main_keyboard())
