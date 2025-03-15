from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from schemas.user import UserSchema


async def authenticate(user_data: UserSchema, session: AsyncSession) -> UserSchema:
    user = await session.scalar(select(User).filter(User.id == user_data.id))
    if user:
        return UserSchema.model_validate(user)

    new_user = User(**user_data.model_dump())

    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserSchema.model_validate(new_user)
    except SQLAlchemyError as e:
        await session.rollback()
        raise e


async def get_user_progress(user_id: int, session: AsyncSession): ...
