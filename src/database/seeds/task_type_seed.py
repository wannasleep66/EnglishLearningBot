import logging

from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Topic, TaskType


class TaskTypeSeeder:
    @staticmethod
    async def apply(session: AsyncSession):
        task_types = [
            {
                "name": "Задание закрытого типа",
                "description": "",
            },
            {
                "name": "Задание на установление соответствия",
                "description": "",
            },
            {
                "name": "Задания на установление последовательности",
                "description": "",
            },
            {
                "name": "Задания на краткий открытый ответ",
                "description": "",
            },
        ]

        session.add_all(
            [
                TaskType(
                    name=task_type.get("name"), description=task_type.get("description")
                )
                for task_type in task_types
            ]
        )
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(str(e))

    @staticmethod
    async def undo(session: AsyncSession):
        stmt = delete(TaskType)
        try:
            await session.execute(stmt)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(str(e))
