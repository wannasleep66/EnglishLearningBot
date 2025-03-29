from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import transaction
from schemas.task import TaskSchema
from telegram.base.constants import KeyboardCommands, CallBacks
from src.services import exercise_service
from telegram.tasks.keyboards import (
    topics_selection,
    regenerate_task_button,
    cancel_task_button,
    back_to_topics_button,
)
from telegram.tasks.state import ExerciseState

tasks_router = Router()


@tasks_router.message(F.text == KeyboardCommands.tasks)
@transaction
async def get_topics_to_select(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    topics = await exercise_service.get_topics(session)
    await state.set_state(ExerciseState.topic_selection)
    await message.answer(
        text="Список доступных тем", reply_markup=topics_selection(topics)
    )


@tasks_router.callback_query(F.data.startswith("topic-"), ExerciseState.topic_selection)
@transaction
async def handle_topic_selection(
    call: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    await call.answer()

    topic_id = int(call.data.split("-")[1])
    if not topic_id:
        await call.message.answer(
            "Произошла ошибка при выборе темы, попробуйте еще раз"
        )
        await state.clear()
        return

    await state.update_data(topic_id=topic_id)
    task = await exercise_service.get_task(topic_id, session)
    if not task:
        await call.message.answer("Произошла ошибка при генерации задачи")
        return

    await state.set_state(ExerciseState.verify)
    await state.update_data(task=task.model_dump())
    await call.message.answer(text=task.task, reply_markup=regenerate_task_button())


@tasks_router.message(F.text, ExerciseState.verify)
@transaction
async def handle_user_answer(
    message: Message, state: FSMContext, session: AsyncSession
) -> None:
    try:
        task_data = await state.get_value("task")
        current_task = TaskSchema(**task_data)
    except ValueError:
        await message.answer("Неожиданная ошибка, попробуйте еще раз")
        return

    is_correct = await exercise_service.check_answer(
        user_id=str(message.from_user.id),
        answer=message.text,
        task=current_task,
        session=session,
    )

    if is_correct:
        await state.set_state(ExerciseState.topic_selection)
        await message.answer(
            "Правильно, вы молодец!", reply_markup=back_to_topics_button()
        )
        return

    await message.answer(
        "Неверно, можете попробовать еще раз или попробовать в следующий раз!",
        reply_markup=cancel_task_button(),
    )


@tasks_router.callback_query(F.data == CallBacks.back_to_topic_selection)
@transaction
async def return_to_topic_selection(
    call: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    topics = await exercise_service.get_topics(session)
    await state.set_state(ExerciseState.topic_selection)
    await call.message.edit_text(
        text="Список доступных тем", reply_markup=topics_selection(topics)
    )


@tasks_router.callback_query(F.data == CallBacks.regenerate_task)
@transaction
async def regenerate_task(
    call: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    await call.answer()
    task_dict = await state.get_value("task")
    if not task_dict:
        await call.answer(text="Ошибка, не удалось перегенировать задание")
        return

    try:
        task_data = TaskSchema(**task_dict)
    except ValueError:
        await call.answer(text="Ошибка, не удалось перегенировать задание")
        return

    task = await exercise_service.get_task(task_data.topic.id, session)
    if not task:
        await call.message.answer("Произошла ошибка при генерации задачи")
        return

    await state.update_data(task=task.model_dump())
    await state.set_state(ExerciseState.verify)
    await call.message.edit_text(text=task.task, reply_markup=regenerate_task_button())


@tasks_router.callback_query(F.data == CallBacks.cancel_task, ExerciseState.verify)
async def cancel_task(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await state.set_state(ExerciseState.topic_selection)
    await call.message.delete()
