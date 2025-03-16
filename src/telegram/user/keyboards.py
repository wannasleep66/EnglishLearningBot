from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from schemas.topic import TopicSchema
from telegram.base.constants import KeyboardCommands, CallBacks


def main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=KeyboardCommands.tasks)
    kb.button(text=KeyboardCommands.profile)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def to_topics_progress(text: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=text, callback_data=CallBacks.topic_progress)
    kb.adjust(1)
    return kb.as_markup()


def topics_progress_selection(topics: list[TopicSchema]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for topic in topics:
        kb.button(text=topic.name, callback_data=f"topic_progress-{topic.id}")
    kb.button(text="Назад", callback_data=CallBacks.back_to_profile)
    kb.adjust(1)
    return kb.as_markup()
