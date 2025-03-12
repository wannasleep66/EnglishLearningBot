from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.settings.settings import settings
from telegram.handlers import composer

bot = Bot(token=settings.telegram.bot_token, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(composer)


async def bootstrap() -> None:
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
