from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from src.settings.settings import settings
from .tasks.handler import tasks_router
from .user.handler import user_router

bot = Bot(
    token=settings.telegram.bot_token,
    default=DefaultBotProperties(parse_mode="HTML"),
)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(user_router)
dp.include_router(tasks_router)


async def bootstrap() -> None:
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
