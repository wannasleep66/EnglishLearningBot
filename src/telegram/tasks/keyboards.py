from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from schemas.task import TaskType
from schemas.topic import TopicSchema
from telegram.base.constants import CallBacks


def topics_selection(topics: list[TopicSchema]) -> InlineKeyboardMarkup:
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
    kb.button(text="Назад", callback_data=CallBacks.back_to_topic_selection)
    kb.adjust(3)
    return kb.as_markup()


def regenerate_task_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Сгенерировать другое", callback_data=CallBacks.regenerate_task)
    kb.adjust(1)
    return kb.as_markup()


def cancel_task_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Прекратить", callback_data=CallBacks.cancel_task)
    kb.adjust(1)
    return kb.as_markup()
