from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Добавить задачу"), KeyboardButton(text="Список задач")],
        [KeyboardButton(text="Найти задачу")],
        [KeyboardButton(text="Отметить выполненной")],
        [KeyboardButton(text="Удалить завершённые")],
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
