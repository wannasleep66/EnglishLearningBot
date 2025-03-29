from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import transaction
from schemas.user import UserSchema
from src.services import user_service, exercise_service
from telegram.base.constants import KeyboardCommands, CallBacks
from telegram.user.keyboards import (
    main_keyboard,
    to_topics_progress,
    topics_progress_selection,
    profile_keyboard,
)

user_router = Router()


@user_router.message(CommandStart())
@transaction
async def start_command(message: Message, session: AsyncSession) -> None:
    user = await user_service.authenticate(
        UserSchema(
            id=str(message.from_user.id),
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        ),
        session,
    )
    await message.answer(f"Привет {user.username}", reply_markup=main_keyboard())


@user_router.message(F.text == KeyboardCommands.profile)
@transaction
async def show_profile(message: Message, session: AsyncSession) -> None:
    user_progress = await user_service.get_user_progress(
        str(message.from_user.id), session
    )
    user_progress_message = (
        f"<b>{user_progress.username}</b> Ваш прогресс\n\n"
        f"<b>Общее количество данных ответов</b>: {user_progress.total_answers}\n\n"
        f"<b>Количество правильных ответов</b>: {user_progress.total_correct_answers}\n\n"
        f"<b>Количество неверных ответов</b>: {user_progress.total_incorrect_answers}\n\n"
        f"<b>Лучшая тема</b>: {user_progress.best_topic if user_progress.best_topic else "У вас еще нету лучшей темы..."}"
    )
    await message.answer(
        user_progress_message,
        reply_markup=profile_keyboard(user_progress.has_notifications),
    )


@user_router.callback_query(F.data == CallBacks.topic_progress)
@transaction
async def get_topics_to_show_progress(
    call: CallbackQuery, session: AsyncSession
) -> None:
    await call.answer()
    topics = await exercise_service.get_topics(session)
    await call.message.edit_text(
        "Выберите тему, по которой хотите узнать свой прогресс",
        reply_markup=topics_progress_selection(topics),
    )


@user_router.callback_query(F.data.startswith("topic_progress-"))
@transaction
async def get_topic_progress(call: CallbackQuery, session: AsyncSession) -> None:
    await call.answer()
    topic_id = int(call.data.split("-")[1])
    if not topic_id:
        await call.message.answer("Прозошла ошибка при выборе темы, попробуйте еще раз")
        return

    topic_progress = await user_service.get_user_topic_progres(
        str(call.from_user.id), topic_id, session
    )
    topic_progress_message = (
        (
            f"<b>Прогресс по теме</b> <i>{topic_progress.topic.name}</i>\n"
            f"{topic_progress.topic.description}\n\n"
            f"<b>Общее количество данных ответов</b>: {topic_progress.total_answers}\n\n"
            f"<b>Количество правильных ответов</b>: {topic_progress.total_correct_answers}\n\n"
            f"<b>Количество неверных ответов</b>: {topic_progress.total_incorrect_answers}\n\n"
        )
        if topic_progress
        else "<i>Вы еще не решали задачи по этой теме</i>"
    )
    await call.message.edit_text(
        topic_progress_message, reply_markup=to_topics_progress()
    )


@user_router.callback_query(F.data == CallBacks.back_to_profile)
@transaction
async def return_to_profile(call: CallbackQuery, session: AsyncSession) -> None:
    await call.answer()
    user_progress = await user_service.get_user_progress(
        str(call.from_user.id), session
    )
    user_progress_message = (
        f"<b>{user_progress.username}</b> Ваш прогресс\n\n"
        f"<b>Общее количество данных ответов</b>: {user_progress.total_answers}\n\n"
        f"<b>Количество правильных ответов</b>: {user_progress.total_correct_answers}\n\n"
        f"<b>Количество неверных ответов</b>: {user_progress.total_incorrect_answers}\n\n"
        f"<b>Лучшая тема</b>: {user_progress.best_topic if user_progress.best_topic else "У вас еще нету лучшей темы..."}"
    )
    await call.message.edit_text(
        user_progress_message,
        reply_markup=profile_keyboard(user_progress.has_notifications),
    )


@user_router.callback_query(F.data == CallBacks.notifications_switch)
@transaction
async def handle_notifications_switch(
    call: CallbackQuery, session: AsyncSession
) -> None:
    updated_user = await user_service.switch_user_notifications(
        str(call.from_user.id), session
    )
    if not updated_user:
        await call.answer(text="Что то пошло не так...")

    await call.answer(
        text=(
            "Уведомления влючены"
            if updated_user.has_notifications
            else "Уведомления выключены"
        )
    )

    await return_to_profile(call)
