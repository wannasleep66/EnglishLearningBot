from pydantic import BaseModel

from schemas.topic import TopicSchema
from schemas.user import UserSchema


class AnswerSchema(BaseModel):
    user: UserSchema
    topic: TopicSchema
    task: str
    is_correct: bool


class AnswerCreateSchema(BaseModel):
    user_id: str
    topic_id: int
    task: str
    is_correct: bool
