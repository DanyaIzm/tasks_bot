from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import formatting

from keyboards.main_keyboard import get_main_keyboard
from models import User
from repositories.repository import UserRepository

from .states import RegistrationForm

router = Router()


@router.message(Command("start"))
@router.message(F.text == "register")
async def registration_handler(
    message: Message, state: FSMContext, user_repository: UserRepository
):
    user = user_repository.find(id=message.from_user.id)

    if user is not None:
        await message.answer(
            "Используйте кнопки снизу или команды", reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            **formatting.as_section(
                "Отлично. Ниже описаны правила регистрации:",
                formatting.Italic(
                    "Длина имени должна быть между 3 и 15 символами. Телефон должен быть в формате 88005553535 или +78005553535"
                ),
            ).as_kwargs()
        )
        await message.answer("Напишите своё имя")

        await state.set_state(RegistrationForm.name)


@router.message(RegistrationForm.name)
async def registration_name_step_handler(message: Message, state: FSMContext):
    await state.update_data({"name": message.text})

    await state.set_state(RegistrationForm.phone)

    await message.answer("Теперь напиши номер телефона (88005553535 или +78005553535)")


@router.message(RegistrationForm.phone)
async def registration_phone_step_handler(
    message: Message, state: FSMContext, user_repository: UserRepository
):
    await state.update_data({"phone": message.text})

    user_data = await state.get_data()

    try:
        user = User(id=message.from_user.id, **user_data)

        user_repository.add_user(user)

        await message.answer("Вы успешно зарегистрировались")

        await message.answer(
            "Используйте кнопки снизу или команды", reply_markup=get_main_keyboard()
        )
    except ValueError:
        await message.answer(
            "Вы ввели неправильные данные. Проверьте номер телефона и введённое имя"
        )
    finally:
        await state.clear()
