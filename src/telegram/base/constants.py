from dataclasses import dataclass


@dataclass(frozen=True)
class KeyboardCommands:
    profile = "Профиль"
    tasks = "Упражнения"


@dataclass(frozen=True)
class CallBacks:
    back_to_topic_selection = "to_topics"
    back_to_types_selection = "to_types"
    regenerate_task = "regenerate"
    cancel_task = "cancel_task"

    topic_progress = "topic_progress"
    back_to_profile = "to_profile"
