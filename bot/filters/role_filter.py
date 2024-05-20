from typing import Union, Collection, Callable, Dict, Any, Awaitable

from aiogram.filters import BaseFilter
from aiogram.types import Message, TelegramObject

from bot.database.role import UserRole


class RoleFilter(BaseFilter):
    def __init__(self, role: Union[None, UserRole, Collection[UserRole]] = None):
        if role is None:
            self.roles = None
        elif isinstance(role, UserRole):
            self.roles = {role}
        else:
            self.roles = set(role)

    async def __call__(
            self,
            event: TelegramObject,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            **data
    ) -> bool:
        if self.roles is None:
            return True
        return data.get("role") in self.roles
