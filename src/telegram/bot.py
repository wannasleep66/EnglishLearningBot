from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from src.settings.settings import settings
from .middlewares import activity_recorder_middleware
from .notifications import scheduler, notify_inactive_users
from .tasks.handler import tasks_router
from .user.handler import user_router

bot = Bot(
    token=settings.telegram.bot_token,
    default=DefaultBotProperties(parse_mode="HTML"),
)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(user_router)
dp.include_router(tasks_router)
dp.update.outer_middleware(middleware=activity_recorder_middleware)


async def on_startup() -> None:
    scheduler.start()
    scheduler.add_job(
        notify_inactive_users,
        trigger="interval",
        minutes=1,
        id="check_inactive_users",
        replace_existing=True,
    )


async def on_shutdown() -> None:
    scheduler.shutdown()


async def bootstrap() -> None:
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await on_startup()
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await on_shutdown()
        await bot.session.close()
