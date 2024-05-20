from aiogram.fsm.state import StatesGroup, State


class MovieState(StatesGroup):
    code = State()
