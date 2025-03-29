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


def profile_keyboard(has_notifications: bool) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Подробнее", callback_data=CallBacks.topic_progress)
    kb.button(
        text="Отключить уведомления" if has_notifications else "Включить уведомления",
        callback_data=CallBacks.notifications_switch,
    )
    kb.adjust(2)
    return kb.as_markup()


def to_topics_progress() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад", callback_data=CallBacks.topic_progress)
    kb.adjust(1)
    return kb.as_markup()


def topics_progress_selection(topics: list[TopicSchema]) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for topic in topics:
        kb.button(
            text=topic.name, callback_data=f"{CallBacks.topic_progress}-{topic.id}"
        )
    kb.button(text="Назад", callback_data=CallBacks.back_to_profile)
    kb.adjust(1)
    return kb.as_markup()
