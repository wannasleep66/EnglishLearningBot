import asyncio

from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Topic
from database.session import session_factory


class TopicSeeder:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def apply(self):
        topics = [
            {
                "name": "Простые времена глагола",
                "description": "Студенты знакомятся с основными временами английского языка: Present Simple, Past Simple и Future Simple. Они учатся различать эти времена по структуре и использованию. Также рассматриваются ключевые отличия между ними при описании действий в настоящем, прошлом и будущем..",
            },
            {
                "name": "Вопросительные конструкции",
                "description": "Изучается структура формирования вопросов в английском языке. Основные типы вопросов: общие (yes/no questions), специальные (wh-questions), альтернативные и разделительные. Разбираются способы изменения порядка слов в вопросе.",
            },
            {
                "name": "Чтение",
                "description": "Развитие навыков чтения на английском языке.",
            },
            {
                "name": "Письмо",
                "description": "Практика написания текстов на английском языке.",
            },
            {
                "name": "Разговорная практика",
                "description": "Упражнения для улучшения разговорных навыков.",
            },
            {
                "name": "Прослушивание",
                "description": "Развитие навыков восприятия на слух.",
            },
            {
                "name": "Культура",
                "description": "Изучение культурных аспектов англоговорящих стран.",
            },
        ]

        topic_models = [
            Topic(name=topic.get("name"), description=topic.get("description"))
            for topic in topics
        ]
        self.session.add_all(topic_models)
        try:
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def undo(self):
        stmt = delete(Topic)
        try:
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise


async def seed():
    async with session_factory() as session:
        topic_seeder = TopicSeeder(session)
        await topic_seeder.apply()


if __name__ == "__main__":
    asyncio.run(seed())
