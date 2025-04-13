from datetime import datetime

from asyncpg.pgproto.pgproto import timedelta
from sqlalchemy import select, func, case, desc, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, Answer, Topic
from schemas.topic import TopicSchema
from schemas.user import UserSchema, UserProgressSchema, UserTopicProgressSchema
from settings.settings import settings


async def authenticate(user_data: UserSchema, session: AsyncSession) -> UserSchema:
    user = await session.scalar(select(User).filter(User.id == user_data.id))
    if user:
        return UserSchema.model_validate(user)

    new_user = User(**user_data.model_dump())

    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserSchema.model_validate(new_user)
    except SQLAlchemyError as e:
        await session.rollback()
        raise e


async def get_inactive_users(session: AsyncSession) -> list[UserSchema]:
    query = select(User).filter(
        and_(
            User.last_activity
            < datetime.now()
            - timedelta(minutes=settings.notifications.notify_after_minutes),
            User.has_notifications == True,
        )
    )
    inactive_users = await session.scalars(query)
    return list(UserSchema.model_validate(user) for user in inactive_users)


async def update_user_activity(user_id: str, session: AsyncSession) -> None:
    query = select(User).filter(
        and_(User.id == user_id, User.has_notifications == True)
    )
    user_to_update = await session.scalar(query)
    if not user_to_update:
        return

    user_to_update.last_activity = datetime.now()

    try:
        await session.commit()
        await session.refresh(user_to_update)
    except SQLAlchemyError:
        await session.rollback()
        raise


async def switch_user_notifications(
    user_id: str, session: AsyncSession
) -> UserSchema | None:
    user_to_update = await session.scalar(select(User).filter(User.id == user_id))
    if not user_to_update:
        return

    user_to_update.has_notifications = not user_to_update.has_notifications

    try:
        await session.commit()
        await session.refresh(user_to_update)
    except SQLAlchemyError:
        await session.rollback()
        raise

    return UserSchema.model_validate(user_to_update)


async def get_user_progress(user_id: str, session: AsyncSession):
    topic_stats_query = (
        select(
            Answer.user_id,
            Topic.name,
            func.sum(case((Answer.is_correct, 1), else_=0)).label("correct_answers"),
            func.sum(case((~Answer.is_correct, 1), else_=0)).label("incorrect_answers"),
            func.count().label("total_answers"),
        )
        .join(Topic, Answer.topic_id == Topic.id)
        .group_by(Answer.user_id, Topic.name)
        .alias("topic_stats")
    )

    best_topic_query = (
        select(topic_stats_query.c.name)
        .filter(User.id == topic_stats_query.c.user_id)
        .order_by(desc(topic_stats_query.c.correct_answers))
        .limit(1)
        .correlate(User)
    )

    query = (
        select(
            User.id,
            User.username,
            User.has_notifications,
            func.coalesce(func.sum(topic_stats_query.c.total_answers), 0).label(
                "total_answers"
            ),
            func.coalesce(func.sum(topic_stats_query.c.correct_answers), 0).label(
                "total_correct_answers"
            ),
            func.coalesce(func.sum(topic_stats_query.c.incorrect_answers), 0).label(
                "total_incorrect_answers"
            ),
            best_topic_query.scalar_subquery().label("best_topic"),
        )
        .outerjoin(topic_stats_query, User.id == topic_stats_query.c.user_id)
        .filter(User.id == user_id)
        .group_by(User.id)
    )

    result = await session.execute(query)
    row = result.mappings().first()
    return UserProgressSchema.model_validate(row)


async def get_user_topic_progres(user_id: str, topic_id: int, session: AsyncSession):
    topic_stats_query = (
        select(
            Answer.user_id,
            Topic,
            func.sum(case((Answer.is_correct, 1), else_=0)).label("correct_answers"),
            func.sum(case((~Answer.is_correct, 1), else_=0)).label("incorrect_answers"),
            func.count().label("total_answers"),
        )
        .join(Topic, Answer.topic_id == Topic.id)
        .filter(and_(Topic.id == topic_id, Answer.user_id == user_id))
        .group_by(Answer.user_id, Topic.id, Topic.name, Topic.description)
    )

    result = await session.execute(topic_stats_query)
    row = result.mappings().first()
    return (
        UserTopicProgressSchema(
            topic=TopicSchema.model_validate(row.get("Topic", "")),
            total_answers=row.get("total_answers", 0),
            total_correct_answers=row.get("correct_answers", 0),
            total_incorrect_answers=row.get("incorrect_answers", 0),
        )
        if row
        else None
    )
