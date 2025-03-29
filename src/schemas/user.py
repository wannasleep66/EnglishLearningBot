from pydantic import BaseModel, ConfigDict, Field

from schemas.topic import TopicSchema


class UserSchema(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    has_notifications: bool = Field(default=False)

    model_config = ConfigDict(from_attributes=True)


class UserTopicProgressSchema(BaseModel):
    topic: TopicSchema
    total_answers: int
    total_correct_answers: int
    total_incorrect_answers: int


class UserProgressSchema(BaseModel):
    username: str
    has_notifications: bool
    total_answers: int
    total_correct_answers: int
    total_incorrect_answers: int
    best_topic: str | None

    model_config = ConfigDict(from_attributes=True)
