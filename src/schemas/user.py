from typing import Dict

from pydantic import BaseModel, ConfigDict

from schemas.task import TaskType
from schemas.topic import TopicSchema


class UserSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)


class UserTopicProgressSchema(BaseModel):
    topic: TopicSchema
    total_answers: int
    total_correct_answers: int
    total_incorrect_answers: int


class UserProgressSchema(BaseModel):
    username: str
    total_answers: int
    total_correct_answers: int
    total_incorrect_answers: int
    best_topic: str

    model_config = ConfigDict(from_attributes=True)
