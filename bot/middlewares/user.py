from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from bot.config import Config
from bot.database.models import User


class UserMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: dict[str, Any]
    ) -> Any:
        user = event.from_user
        session: AsyncSession = data["session"]
        config: Config = data["config"]
        db_user = (await session.execute(Select(User).where(User.telegram_id == user.id))).scalars().first()
        if not db_user:
            db_user = User(telegram_id=user.id)
            session.add(db_user)
            await session.commit()
            for admin_id in config.tg_bot.admin_ids:
                await event.bot.send_message(admin_id, f"👤 <b>Новый пользователь</b>\n\n<b>Username:</b> {'@'+user.username if user.username else 'Отсутствует'}\n<b>Full Name:</b> <code>{user.full_name}</code>\n<b>ID:</b> <code>{user.id}</code>")

        data["user"] = db_user
        return await handler(event, data)
