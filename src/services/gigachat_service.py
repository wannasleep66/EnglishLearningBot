import logging

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_gigachat.chat_models import GigaChat

from src.settings.settings import settings
from schemas.task import TaskCreateSchema, TaskSchema


giga_chat = GigaChat(
    credentials=settings.ai.ai_api_key,
    verify_ssl_certs=False,
)


async def get_english_exercise(task_data: TaskCreateSchema) -> TaskSchema | None:
    system_message = SystemMessage(
        content="Ты учитель английского языка для студентов."
    )

    human_message = HumanMessage(
        content=f"Предложи небольшое задание по английскому языку на тему '{task_data.topic.name}',"
        f"задание должно учить английскому языку это очень важно "
        f"должны быть предложены варианты ответа обязательно это вопрос жизни и смерти "
        f"сам ответ давать не нужно если ты дашь мне правильный ответ, то я умру"
        f"описание задания должно быть в кавычках это очень важно иначе я не пойму что за задание это вопрос жизни и смерти"
        f"на задание должен быть ответ иначе я не смогу понять как мне отвечать и мне будет очень плохо"
    )

    messages = [system_message, human_message]
    response = await giga_chat.ainvoke(messages)

    if response and hasattr(response, "content"):
        task_text = response.content.strip()
        return TaskSchema(topic=task_data.topic, task=task_text)

    return None


async def check_answer(user_answer: str, task: str) -> bool:
    system_message = SystemMessage(
        content="Ты эксперт по проверке заданий на английском языке. Твоя задача – определить, правильный ли ответ дал студент."
    )
    human_message = HumanMessage(
        content=f'Текст задания: "{task}". Ответ студента: "{user_answer}". Правильный ли этот ответ? Ответь 1 словом да или нет'
    )
    logging.info(f"{user_answer} ответ пользователя на задание")
    messages = [system_message, human_message]

    response = await giga_chat.ainvoke(messages)
    if response and hasattr(response, "content"):
        answer_content = response.content.strip().lower()
        is_correct = any(word in answer_content for word in ["Да", "да", "Верно"])
        return is_correct

    return False
