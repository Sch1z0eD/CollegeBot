from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder



def start_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="Найти фильм", callback_data='search')
    return builder.as_markup(resize_keyboard=True)