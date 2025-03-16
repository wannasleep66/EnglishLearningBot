from enum import StrEnum, auto
from typing import Type

from pydantic import BaseModel

from schemas.topic import TopicSchema


class TaskType(StrEnum):
    translate = auto()
    grammatical = auto()
    reading = auto()


class TaskCreateSchema(BaseModel):
    topic: TopicSchema
    type: TaskType | Type[TaskType]


class TaskSchema(BaseModel):
    topic: TopicSchema
    type: TaskType
    task: str
