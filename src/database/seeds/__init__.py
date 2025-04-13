__all__ = (
    "TopicSeeder",
    "TaskTypeSeeder",
    "TaskExampleSeeder",
)


import asyncio

from sqlalchemy import select

from database.models import Topic, TaskType
from src.database.seeds.task_type_seed import TaskTypeSeeder
from src.database.seeds.task_example_seed import TaskExampleSeeder
from src.database.seeds.topic_seed import TopicSeeder
from src.database.session import session_factory


async def seed() -> None:
    async with session_factory() as session:
        # await TopicSeeder.undo(session)
        # await TaskTypeSeeder.undo(session)
        # await TopicSeeder.apply(session)
        # await TaskTypeSeeder.apply(session)
        # await TaskExampleSeeder.undo(session)
        # await TaskExampleSeeder.apply(session)
        print(
            list(
                {"id": topic.id, "name": topic.name}
                for topic in await session.scalars(select(Topic))
            )
        )
        print(
            list(
                {"id": task_type.id, "name": task_type.name}
                for task_type in await session.scalars(select(TaskType))
            )
        )
        await session.close()


if __name__ == "__main__":
    asyncio.run(seed())
