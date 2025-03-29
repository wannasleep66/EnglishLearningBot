from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from schemas.topic import TopicSchema
from telegram.base.constants import CallBacks


def topics_selection(topics: list[TopicSchema]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for topic in topics:
        kb.button(text=topic.name, callback_data=f"topic-{topic.id}")
    kb.adjust(1)
    return kb.as_markup()


def back_to_topics_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="К списку тем", callback_data=CallBacks.back_to_topic_selection)
    kb.adjust(1)
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
