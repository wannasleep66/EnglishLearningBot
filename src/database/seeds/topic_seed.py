import logging

from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Topic


class TopicSeeder:
    @staticmethod
    async def apply(session: AsyncSession):
        topics = [
            {
                "name": "Глагол to be в настоящем простом времени (Present Simple) ",
                "description": "",
            },
            {
                "name": "Неопределенные артикли a и an",
                "description": "",
            },
            {
                "name": "Предлоги времени",
                "description": "",
            },
            {
                "name": "Настоящее простое время (Present Simple) в утвердительных предложениях",
                "description": "",
            },
        ]

        topic_models = [
            Topic(name=topic.get("name"), description=topic.get("description"))
            for topic in topics
        ]
        session.add_all(topic_models)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(str(e))

    @staticmethod
    async def undo(session: AsyncSession):
        stmt = delete(Topic)
        try:
            await session.execute(stmt)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(str(e))
