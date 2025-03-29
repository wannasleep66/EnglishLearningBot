from aiogram.fsm.state import State, StatesGroup


class ExerciseState(StatesGroup):
    topic_selection = State()
    verify = State()
