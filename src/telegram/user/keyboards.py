from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from telegram.common import KeyboardCommands


def main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=KeyboardCommands.tasks)
    kb.button(text=KeyboardCommands.profile)
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
