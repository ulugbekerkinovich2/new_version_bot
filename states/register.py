from aiogram.dispatcher.filters.state import StatesGroup, State


class Register(StatesGroup):
    name = State()
    number = State()


class Children_Register(StatesGroup):
    name = State()
    number = State()


class Children_Link(StatesGroup):
    telegram_id = State()
    link = State()


class Set_Link(StatesGroup):
    name = State()
    link = State()
