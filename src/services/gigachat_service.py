from openai import AsyncOpenAI
from aiohttp import ClientSession
from src.settings.settings import settings
from schemas.task import TaskCreateSchema, TaskSchema


api = AsyncOpenAI(api_key=settings.ai.ai_api_key, base_url=settings.ai.ai_base_url)


async def get_english_exercise(task_data: TaskCreateSchema) -> TaskSchema | None:
    system_prompt = "Ты агент учитель английского языка для студентов"
    user_prompt = f"Дай задание по теме:  {task_data.topic.name},  с типом задания: {task_data.type.value}, дай пояснения как отвечать на задание, чтобы когда я прислал тебе ответ ты мог легко сказать правильно или нет"

    response = await api.chat.completions.create(
        model="mistralai/Mistral-7B-Instruct-v0.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=100,
    )

    if len(response.choices) > 0:
        task_text = response.choices[0].message.content.strip()
        return TaskSchema(topic=task_data.topic, type=task_data.type, task=task_text)

    return None


def check_answer(user_answer: str, correct_answer: str) -> bool:
    return user_answer.strip().lower() == correct_answer.strip().lower()
