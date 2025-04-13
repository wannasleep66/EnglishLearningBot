import logging

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Topic, Answer, TaskType, TaskExample
from schemas.answer import AnswerCreateSchema
from schemas.task import TaskSchema, TaskCreateSchema
from schemas.task_type import TaskTypeSchema
from schemas.topic import TopicSchema
from services import gigachat_service


async def get_topics(session: AsyncSession) -> list[TopicSchema]:
    query = select(Topic).order_by(Topic.id)
    topics = await session.scalars(query)
    return list(TopicSchema.model_validate(topic) for topic in topics)


async def get_task_types(session: AsyncSession) -> list[TaskTypeSchema]:
    query = select(TaskType).order_by(TaskType.id)
    task_types = await session.scalars(query)
    return list(TaskTypeSchema.model_validate(task_type) for task_type in task_types)


async def get_task(
    topic_id: int, task_type_id: int, session: AsyncSession
) -> TaskSchema | None:
    query = (
        select(TaskExample)
        .options(joinedload(TaskExample.topic), joinedload(TaskExample.task_type))
        .filter(
            and_(
                TaskExample.task_type_id == task_type_id,
                TaskExample.topic_id == topic_id,
            )
        )
    )
    task_example = await session.scalar(query)
    if not task_example:
        return None

    task = await gigachat_service.get_english_exercise(
        TaskCreateSchema(
            task_type=task_example.task_type,
            topic=task_example.topic,
            example=task_example.text,
        )
    )
    if not task:
        return None

    return task


async def check_answer(
    user_id: str, answer: str, task: TaskSchema, session: AsyncSession
) -> bool:
    is_correct = await gigachat_service.check_answer(user_answer=answer, task=task.task)
    answer_from_giga = AnswerCreateSchema(
        task=task.task, user_id=user_id, topic_id=task.topic.id, is_correct=is_correct
    )
    new_answer = Answer(**answer_from_giga.model_dump())

    try:
        session.add(new_answer)
        await session.commit()
        await session.refresh(new_answer)
    except SQLAlchemyError:
        await session.rollback()
        raise

    return new_answer.is_correct
