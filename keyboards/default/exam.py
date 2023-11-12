from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db
from utils.misc.mix import row_2_col


def get_subjects_kb(user_id):
    rows = db.select_user_subjects(user_id, only_selected=True)
    rows = row_2_col(rows)
    buttons = []
    keyboard = []
    for columns in rows:
        for column in columns:
            buttons.append(
                KeyboardButton(text=f'📚 {column[1]}')
            )
        keyboard.append(buttons)
        buttons = []
    keyboard[-1].append(KeyboardButton(text="⬅ Orqaga"))
    return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard)

