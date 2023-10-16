from aiogram.dispatcher.filters.state import StatesGroup, State


class EditState(StatesGroup):
    Telefon = State()
    FIO = State()
    Region = State()
    University = State()