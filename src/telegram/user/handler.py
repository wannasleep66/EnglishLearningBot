from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import transaction
from schemas.user import UserSchema
from src.services import user_service
from telegram.common import KeyboardCommands
from telegram.user.keyboards import main_keyboard

user_router = Router()


@user_router.message(CommandStart())
@transaction
async def start_command(message: Message, session: AsyncSession):
    user = await user_service.authenticate(
        UserSchema(
            id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        ),
        session,
    )
    await message.answer(f"Привет {user.username}", reply_markup=main_keyboard())


@user_router.message(F.text == KeyboardCommands.profile)
@transaction
async def show_profile(message: Message, session: AsyncSession):
    await message.answer("Тут будет твой профиль работяга")
