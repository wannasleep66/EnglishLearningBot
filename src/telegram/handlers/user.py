from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import transaction
from schema.user import UserSchema
from src.services import user_service


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
    await message.answer(f"Привет {user.username}")
