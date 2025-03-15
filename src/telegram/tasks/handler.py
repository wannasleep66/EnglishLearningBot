from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import transaction
from telegram.common import KeyboardCommands


tasks_router = Router()


@tasks_router.message(F.text == KeyboardCommands.tasks)
@transaction
async def show_topics(message: Message, session: AsyncSession):
    await message.answer(text="Щас будет список задачек")
