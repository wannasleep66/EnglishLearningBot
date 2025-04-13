import logging

from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import TaskExample


class TaskExampleSeeder:
    @staticmethod
    async def apply(session: AsyncSession):
        """
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
        """
        task_examples = [
            {
                "topic_id": 116,
                "task_type_id": 65,
                "text": "Выберите правильный вариант отрицания:She _ (not be) a doctor.a)am not,b)is not,c)are not",
            },
            {
                "topic_id": 116,
                "task_type_id": 66,
                "text": "Сопоставьте предложения с их отрицательной формой:1.I am a teacher,2.He is happy,3.We are friends.a) He is not happy.b) We are not friends.c) I am not a teacher.",
            },
            {
                "topic_id": 116,
                "task_type_id": 67,
                "text": "Расположите слова в правильном порядке, чтобы образовать отрицательное предложение:Слова: not, they, are, at home",
            },
            {
                "topic_id": 116,
                "task_type_id": 68,
                "text": "Напишите три предложения о себе: одно утвердительное, одно отрицательное и один вопрос, используя Present Simple.Пример:I like music.I do not play football.Do you speak Spanish?",
            },
            {
                "topic_id": 117,
                "task_type_id": 65,
                "text": "Выберите правильную форму глагола to have:I _ a cat.a)has b)have c)am",
            },
            {
                "topic_id": 117,
                "task_type_id": 66,
                "text": "Сопоставьте подлежащее с правильной формой to have:1.I 2.He 3.We 4.It a)has b)have",
            },
            {
                "topic_id": 117,
                "task_type_id": 67,
                "text": "Постройте правильное утвердительное предложение: Слова: a dog, have, they",
            },
            {
                "topic_id": 117,
                "task_type_id": 68,
                "text": "Напишите три предложения о себе: утвердительное, отрицательное и вопрос с to have. Пример:I have a bicycle.She does not have a laptop.Do you have any pets?",
            },
            {
                "topic_id": 118,
                "task_type_id": 65,
                "text": "Выберите правильный вариант (some / any): There are _ apples in the fridge.a)some b)any",
            },
            {
                "topic_id": 118,
                "task_type_id": 66,
                "text": "Сопоставьте предложения с правильным словом (some / any):I need _ milk for my coffee. Are there _ problems with your phone? There aren’t _ cookies left. a) some b) any",
            },
            {
                "topic_id": 118,
                "task_type_id": 67,
                "text": "Постройте правильное предложение: Слова: any, have, don’t, they, money",
            },
            {
                "topic_id": 118,
                "task_type_id": 68,
                "text": "Напишите три предложения: утвердительное с some, отрицательное с any и вопрос с any.. Пример:There are some books on the table.There isn’t any water in the bottle. Do you have any plans for the weekend??",
            },
            {
                "topic_id": 119,
                "task_type_id": 65,
                "text": "Выберите правильный вариант (too / enough):This coffee is _ hot to drink right now. a)enough b)too",
            },
            {
                "topic_id": 119,
                "task_type_id": 66,
                "text": "Сопоставьте предложения с правильным словом (too / enough): The box is _ heavy for me to lift. We don’t have _ time to finish the project. He is strong _ to win the competition. a)too b)enough",
            },
            {
                "topic_id": 119,
                "task_type_id": 67,
                "text": "Постройте правильное предложение: Слова: too, this, is, spicy, dish",
            },
            {
                "topic_id": 119,
                "task_type_id": 68,
                "text": "Напишите три предложения: одно с too, одно с enough и одно отрицательное с enough.Пример: It’s too cold to go outside. She’s old enough to drive a car. They aren’t rich enough to buy a house.",
            },
            {
                "topic_id": 120,
                "task_type_id": 65,
                "text": "Выберите правильный вариант (There is / There are):_ a book on the table. a) There is b) There are",
            },
            {
                "topic_id": 120,
                "task_type_id": 66,
                "text": "Сопоставьте предложения с правильной формой (There is / There are):_ a pen in my bag._ three cats in the garden. _ some water in the glass. a) There is b) There are",
            },
            {
                "topic_id": 120,
                "task_type_id": 67,
                "text": "Постройте правильное утвердительное предложение: Слова: there, are, chairs, in, room, the, five",
            },
            {
                "topic_id": 120,
                "task_type_id": 68,
                "text": "Напишите три предложения: утвердительное, отрицательное и вопрос с There is/There are: Пример: There is a park near my house. There aren't any eggs in the fridge. Is there a bank on this street?",
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
