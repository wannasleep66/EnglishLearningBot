from aiogram import Router

from .user import user_router

composer = Router()
composer.include_router(user_router)
