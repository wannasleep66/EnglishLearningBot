import logging

from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import TaskExample


class TaskExampleSeeder:
    @staticmethod
    async def apply(session: AsyncSession):
        task_examples = [
            {
                "topic_id": 112,
                "task_type_id": 65,
                "text": "I _ (be) a student.a)am b)is с)are",
            },
            {
                "topic_id": 112,
                "task_type_id": 66,
                "text": "Сопоставьте формы глагола to be с соответствующими лицами и числами:\nI: \nyou: \nhe/she/it: \nwe/they\nВарианты:am,is,are ",
            },
            {
                "topic_id": 112,
                "task_type_id": 67,
                "text": "Расположите слова в правильном порядке, чтобы образовать утвердительное предложение. Слова:student,you,are,a ",
            },
            {
                "topic_id": 112,
                "task_type_id": 68,
                "text": "Напишите короткий текст о себе, используя глагол to be в Present Simple: Опишите себя, используя хотя бы три формы глагола to be (например, I am a student, my friends are from different countries, and we are all happy to learn English together.)",
            },
            {
                "topic_id": 113,
                "task_type_id": 65,
                "text": "Выберите правильный артикль: I have _ book. 1)a,2)an,3)the",
            },
            {
                "topic_id": 113,
                "task_type_id": 66,
                "text": "Сопоставьте артикли a/an с правильными существительными: 1)elephant,2)apple,3)orange,4)dog ",
            },
            {
                "topic_id": 113,
                "task_type_id": 67,
                "text": "Упорядочите слова в предложении, чтобы оно было грамматически правильным: book/a/I/have",
            },
            {
                "topic_id": 113,
                "task_type_id": 68,
                "text": "Напишите короткий текст о вашем дне, используя артикли a и an. Включите как минимум 3 предложения с этими артиклями.Пример(I have a cat named Luna. She is an adorable pet who loves to play. In the morning, I eat an apple for breakfast and drink a cup of coffee). ",
            },
            {
                "topic_id": 114,
                "task_type_id": 65,
                "text": "Выберите все правильные предлоги времени для следующих предложений: The concert starts _ 8 PM. (at/on/in) ",
            },
            {
                "topic_id": 114,
                "task_type_id": 66,
                "text": "Соотнесите следующие временные выражения с правильными предлогами времени: (8 AM, Monday, June, Midnight). Соответствующие предлоги: (at, on, in) ",
            },
            {
                "topic_id": 114,
                "task_type_id": 67,
                "text": "Расположите следующие фразы в правильной последовательности, чтобы описать ваш день, вставив предлоги времени: I have breakfast _ the morning. I go to university _ 8 AM. I usually do homework _ the evening. ",
            },
            {
                "topic_id": 114,
                "task_type_id": 68,
                "text": "Напишите короткий текст о вашем дне, используя предлоги времени at, on и in. Включите как минимум три предложения с этими предлогами.Пример:I usually wake up at 7 AM. On weekdays, I go to work in the morning. In the evening, I like to relax and watch a movie.",
            },
            {
                "topic_id": 115,
                "task_type_id": 65,
                "text": "Выберите правильную форму глагола: My sister _ (to read) a lot of books every day. Варианты ответов:A.reads,B.read,C.is reading,D.to read ",
            },
            {
                "topic_id": 115,
                "task_type_id": 66,
                "text": "Соотнесите слова с правильной формой глагола: 1.I,2.He,3.We,4.She,5.They a)goes,b)go,c)does,d)does,e)go",
            },
            {
                "topic_id": 115,
                "task_type_id": 67,
                "text": "Упорядочите слова в предложении, чтобы оно было грамматически правильным: usually,weekends,I,go,family,my,time,spend,for,walk,a,and,on ",
            },
            {
                "topic_id": 115,
                "task_type_id": 68,
                "text": "Напишите кратко, что вы обычно делаете в субботу и воскресенье, используя слова: Sometimes, often, I like, On Saturdays, watch TV, go for a walk, read novels or magazines, in the park ",
            },
        ]

        session.add_all(
            [
                TaskExample(
                    topic_id=task_example.get("topic_id"),
                    task_type_id=task_example.get("task_type_id"),
                    text=task_example.get("text"),
                )
                for task_example in task_examples
            ]
        )
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(str(e))

    @staticmethod
    async def undo(session: AsyncSession):
        stmt = delete(TaskExample)
        try:
            await session.execute(stmt)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            logging.error(str(e))
