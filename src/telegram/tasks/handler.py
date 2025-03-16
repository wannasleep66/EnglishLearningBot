from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import transaction
from schemas.task import TaskType, TaskSchema
from telegram.base.constants import KeyboardCommands, CallBacks
from src.services import exercise_service
from telegram.tasks.keyboards import (
    topics_selection,
    task_types_inline_keyboard,
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
        await call.message.answer("Прозошла ошибка при выборе темы, попробуйте еще раз")
        await state.clear()
        return

    await state.update_data(topic_id=topic_id)
    await state.set_state(ExerciseState.type_selection)
    topic = await exercise_service.get_topic(topic_id, session)

    await call.message.edit_text(
        text=topic.description, reply_markup=task_types_inline_keyboard()
    )


@tasks_router.callback_query(F.data.startswith("type-"), ExerciseState.type_selection)
@transaction
async def handle_type_selection(
    call: CallbackQuery, state: FSMContext, session: AsyncSession
) -> None:
    await call.answer()
    task_type = TaskType[(call.data.split("-")[1])]
    if not task_type:
        await call.message.answer(
            "Прозошла ошибка при выборе типа задачи, попробуйте еще раз"
        )
        await state.clear()
        return

    topic_id = await state.get_value("topic_id")
    task = await exercise_service.get_task(topic_id, task_type, session)
    if not task:
        await call.message.answer("Прозошла ошибка при генерации задачи")
        return

    await state.set_state(ExerciseState.verify)
    await state.update_data(task=task.model_dump())
    await call.message.answer(text=task.task)


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
        user_id=message.from_user.id,
        answer=message.text,
        task=current_task,
        session=session,
    )

    if is_correct:
        await state.set_state(ExerciseState.type_selection)
        await message.answer("Правильно, вы молодец!")
        return

    await message.answer(
        "Неверно, можете попробовать еще раз или попробовать в следующий раз!"
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
