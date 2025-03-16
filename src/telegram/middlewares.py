import logging
from typing import Dict, Any, Callable, Awaitable

from aiogram.types import Update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import transaction
from services import user_service


@transaction
async def activity_recorder_middleware(
    handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: Dict[str, Any],
    session: AsyncSession,
) -> None:
    user_id = (
        event.message.from_user.id
        if event.message
        else event.callback_query.from_user.id
    )
    try:
        await user_service.update_user_activity(user_id, session)
    except SQLAlchemyError:
        logging.ERROR("Не удалось обновить активность пользователя")

    return await handler(event, data)
