from typing import Callable, Dict, Any, Awaitable

from aiogram.filters import BaseFilter
from aiogram.types import Message, TelegramObject

from bot.config import load_config, Config


class IsAdmin(BaseFilter):
    def __init__(self):
        pass

    async def __call__(
            self,
            event: TelegramObject,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            **data
    ) -> bool:
        config: Config = data['config']
        user = event.from_user
        if user.id in config.tg_bot.admin_ids:
            return True
        return False
