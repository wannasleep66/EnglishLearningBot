from dataclasses import dataclass


@dataclass(frozen=True)
class KeyboardCommands:
    profile = "Профиль"
    tasks = "Упражнения"


@dataclass(frozen=True)
class CallBacks:
    back_to_topic_selection = "to_topics"
    back_to_types_selection = "to_types"
