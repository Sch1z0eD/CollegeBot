from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from bot.config import Config
from bot.database.models import User
from bot.database.role import UserRole


class UserRoleMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        user = event.from_user
        session: AsyncSession = data["session"]
        config: Config = data["config"]
        db_user: User = (await session.execute(Select(User).where(User.telegram_id == user.id))).scalars().first()
        if user.id in config.tg_bot.admin_ids:
            data["role"] = UserRole.ADMIN
        elif db_user:
            data["role"] = UserRole(db_user.role)
        else:
            data["role"] = UserRole.USER
        return await handler(event, data)
