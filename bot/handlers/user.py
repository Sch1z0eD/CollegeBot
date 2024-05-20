import asyncio
import random
from asyncio import sleep
from datetime import datetime, timezone
from typing import List

from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import User
from bot.database.role import UserRole
from bot.filters.IsAdmin import IsAdmin
from bot.filters.role_filter import RoleFilter
from bot.keyboards.user_kb import start_kb
from bot.states.user import MovieState

user_router = Router()


@user_router.message(CommandStart(), IsAdmin())
async def start(message: Message, state: FSMContext, session: AsyncSession, user: User, role: UserRole):
    await state.clear()
    await message.answer(f"Привет! {user.id} - {role.value} - {role}", reply_markup=start_kb())
