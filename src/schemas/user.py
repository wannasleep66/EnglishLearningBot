from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)
