import logging

from aiogram import Bot
from aiogram.exceptions import AiogramError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from settings.settings import settings
from database.session import transaction
from services import user_service

scheduler = AsyncIOScheduler()
bot = Bot(token=settings.telegram.bot_token)


@transaction
async def notify_inactive_users(session: AsyncSession) -> None:
    inactive_users = await user_service.get_inactive_users(session)
    for user in inactive_users:
        try:
            await bot.send_message(chat_id=user.id, text="Какжется пора позаниматься!")
            await user_service.update_user_activity(user.id, session)
        except AiogramError:
            logging.ERROR("Не удалось отправить напоминание пользователю")
        except SQLAlchemyError:
            logging.ERROR("Не удалось обновить активность пользователя")
