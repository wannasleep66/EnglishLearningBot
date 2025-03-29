from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Topic, Answer
from schemas.answer import AnswerCreateSchema
from schemas.task import TaskSchema, TaskCreateSchema
from schemas.topic import TopicSchema
from services import gigachat_service


async def get_topics(session: AsyncSession) -> list[TopicSchema]:
    query = select(Topic).order_by(Topic.id)
    topics = await session.scalars(query)
    return list(TopicSchema.model_validate(topic) for topic in topics)


async def get_topic(topic_id: int, session: AsyncSession) -> TopicSchema | None:
    query = select(Topic).filter(Topic.id == topic_id)
    topic = await session.scalar(query)
    return TopicSchema.model_validate(topic) if topic else None


async def get_task(topic_id: int, session: AsyncSession) -> TaskSchema | None:
    topic = await get_topic(topic_id, session)
    if not topic:
        return None

    task = await gigachat_service.get_english_exercise(TaskCreateSchema(topic=topic))
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
