from pydantic import BaseModel

from schemas.topic import TopicSchema


class TaskCreateSchema(BaseModel):
    topic: TopicSchema


class TaskSchema(BaseModel):
    topic: TopicSchema
    task: str
