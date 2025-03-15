from typing import Dict

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from schemas.task import TaskType
from schemas.topic import TopicSchema


def topics_inline_keyboard(topics: list[TopicSchema]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for topic in topics:
        kb.button(text=topic.name, callback_data=f"topic-{topic.id}")
    kb.adjust(1)
    return kb.as_markup()


def task_types_inline_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=TaskType.reading, callback_data=f"type-{TaskType.reading}")
    kb.button(text=TaskType.translate, callback_data=f"type-{TaskType.reading}")
    kb.button(text=TaskType.grammatical, callback_data=f"type-{TaskType.grammatical}")
    kb.adjust(4)
    return kb.as_markup()
