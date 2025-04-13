from pydantic import BaseModel

from schemas.task_type import TaskTypeSchema
from schemas.topic import TopicSchema


class TaskCreateSchema(BaseModel):
    topic: TopicSchema
    task_type: TaskTypeSchema
    example: str


class TaskSchema(BaseModel):
    topic: TopicSchema
    task_type: TaskTypeSchema
    task: str
