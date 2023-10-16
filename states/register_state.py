from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    Telefon = State()
    FIO = State()
    Region = State()