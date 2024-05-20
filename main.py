import asyncio
import logging

# import uvloop
from aiogram import Dispatcher, Bot, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from bot.config import Config, load_config
from bot.database.models import Base
from bot.handlers import routers_list
from bot.middlewares.database import DbSessionMiddleware
from bot.middlewares.role import UserRoleMiddleware
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.middlewares.user import UserMiddleware

logger = logging.getLogger(__name__)


async def create_pool():
    engine = create_async_engine(f"sqlite+aiosqlite:///db.sqlite3", echo=True, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        return session


def get_storage():
    return MemoryStorage()


def register_global_middlewares(dp: Dispatcher):
    middleware_types = [
        UserMiddleware(),
        UserRoleMiddleware()
        # DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


async def main():
    logging.basicConfig(filename="logs.txt",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    logger.error("Starting bot")
    config: Config = load_config()
    session = await create_pool()
    storage = get_storage()

    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
    ])

    dp = Dispatcher(storage=storage, config=config)
    dp.update.middleware(ThrottlingMiddleware())
    dp.update.middleware(DbSessionMiddleware(session))
    dp.message.filter(F.chat.type == "private")
    register_global_middlewares(dp)
    dp.include_routers(*routers_list)
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        #uvloop.run(main())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
